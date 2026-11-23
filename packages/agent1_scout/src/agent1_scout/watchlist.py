"""Dynamic watchlist seeding, spillover discovery, and weekly pruning for Agent 1."""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping, MutableMapping, Sequence
from dataclasses import dataclass, field, replace
from typing import Any

CHANNELS_LIST_BATCH_SIZE = 50
VIDEOS_LIST_BATCH_SIZE = 50
PLAYLIST_ITEMS_PAGE_SIZE = 10

SUBSCRIBER_COUNT_MIN = 2_000
SUBSCRIBER_COUNT_MAX = 120_000
TARGET_ACTIVE_MIN = 250
TARGET_ACTIVE_MAX = 400

MIN_LONG_FORM_DURATION_SEC = 600
MIN_CRIME_LONG_FORM_IN_LAST_10 = 3
DORMANT_DAYS = 180
DORMANT_MS = DORMANT_DAYS * 24 * 60 * 60 * 1000
YT_TTL_MS = 30 * 24 * 60 * 60 * 1000

DISCOVERED_VIA_SEED = "SEED"
DISCOVERED_VIA_SPILLOVER = "SPILLOVER"

_ISO8601_DURATION = re.compile(
    r"^PT"
    r"(?:(\d+)H)?"
    r"(?:(\d+)M)?"
    r"(?:(\d+(?:\.\d+)?)S)?$"
)

ChannelsList = Callable[..., Mapping[str, Any]]
PlaylistItemsList = Callable[..., Mapping[str, Any]]
VideosList = Callable[..., Mapping[str, Any]]

# YouTube Freebase topic id for Society / Crime (channel topicDetails).
TRUE_CRIME_TOPIC_IDS = frozenset({"/m/0jm_", "/m/04g51"})

_CRIME_KEYWORDS = (
    "true crime",
    "cold case",
    "serial killer",
    "homicide",
    "murder",
    "missing person",
    "unsolved",
    "forensic",
    "investigation",
    "kidnapping",
    "detective",
)

_POP_CULTURE_KEYWORDS = (
    "celebrity gossip",
    "pop culture",
    "movie review",
    "tv recap",
    "entertainment news",
    "reaction video",
    "drama recap",
    "netflix review",
    "celebrity news",
)


class SearchListForbiddenError(RuntimeError):
    """Raised when watchlist seeding or maintenance would call search.list."""


@dataclass(frozen=True, slots=True)
class WatchlistChannel:
    channel_id: str
    uploads_playlist_id: str
    channel_name: str
    subscriber_count: int
    yt_ttl_expires_at: int
    discovered_via: str
    is_active: bool = True
    median_20_views: int = 0
    last_polled_at: int = 0
    last_upload_at_ms: int = 0


@dataclass(frozen=True, slots=True)
class ApiCallLedger:
    search_list_calls: int = 0
    channels_list_calls: int = 0
    playlist_items_list_calls: int = 0
    videos_list_calls: int = 0


@dataclass(frozen=True, slots=True)
class SeedResult:
    admitted: tuple[WatchlistChannel, ...]
    rejected_band: tuple[str, ...]
    ledger: ApiCallLedger


@dataclass(frozen=True, slots=True)
class SpilloverDiscoveryResult:
    promoted: tuple[WatchlistChannel, ...]
    rejected: tuple[str, ...]
    ledger: ApiCallLedger


@dataclass(frozen=True, slots=True)
class PruneResult:
    dormant_deactivated: tuple[str, ...]
    graduated_deactivated: tuple[str, ...]
    ledger: ApiCallLedger


def channel_to_uploads_playlist_id(channel_id: str) -> str:
    """Map a ``UC…`` channel id to its ``UU…`` uploads playlist id."""
    if channel_id.startswith("UC") and len(channel_id) > 2:
        return "UU" + channel_id[2:]
    msg = f"expected UC-prefixed channel id, got {channel_id!r}"
    raise ValueError(msg)


def parse_iso8601_duration(duration: str) -> int:
    if not duration.startswith("PT"):
        msg = f"unsupported duration {duration!r}"
        raise ValueError(msg)
    match = _ISO8601_DURATION.match(duration)
    if not match or match.group(0) == "PT":
        msg = f"unsupported duration {duration!r}"
        raise ValueError(msg)
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = float(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + int(seconds)


def _contains_shorts_hashtag(text: str) -> bool:
    return "#shorts" in text.casefold()


def is_long_form(*, duration_sec: int, title: str, description: str) -> bool:
    if duration_sec < MIN_LONG_FORM_DURATION_SEC:
        return False
    if _contains_shorts_hashtag(title) or _contains_shorts_hashtag(description):
        return False
    return True


def _parse_count(raw: object) -> int | None:
    if raw is None:
        return None
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, str) and raw.isdigit():
        return int(raw)
    return None


def _text_blob(*parts: str) -> str:
    return " ".join(part.casefold() for part in parts if part)


def topic_matches_true_crime(
    *,
    title: str,
    description: str,
    topic_ids: Sequence[str] | None = None,
) -> bool:
    if topic_ids:
        if any(topic_id in TRUE_CRIME_TOPIC_IDS for topic_id in topic_ids):
            return True
    blob = _text_blob(title, description)
    if any(keyword in blob for keyword in _POP_CULTURE_KEYWORDS):
        return False
    return any(keyword in blob for keyword in _CRIME_KEYWORDS)


def title_looks_like_crime_video(title: str, description: str = "") -> bool:
    blob = _text_blob(title, description)
    if any(keyword in blob for keyword in _POP_CULTURE_KEYWORDS):
        return False
    return any(keyword in blob for keyword in _CRIME_KEYWORDS)


def _batched(ids: Sequence[str], size: int) -> list[tuple[str, ...]]:
    return [tuple(ids[index : index + size]) for index in range(0, len(ids), size)]


def _guard_youtube(
    *,
    channels_list: ChannelsList | None,
    playlist_items_list: PlaylistItemsList | None,
    videos_list: VideosList | None,
    ledger: MutableMapping[str, int],
) -> Callable[[str], Mapping[str, Any]]:
    def fetch(method: str, /, **params: Any) -> Mapping[str, Any]:
        if method == "search.list":
            ledger["search_list_calls"] += 1
            raise SearchListForbiddenError(
                "watchlist manager must not call search.list"
            )
        if method == "channels.list":
            if channels_list is None:
                msg = "channels_list callable required"
                raise RuntimeError(msg)
            ledger["channels_list_calls"] += 1
            return channels_list(**params)
        if method == "playlistItems.list":
            if playlist_items_list is None:
                msg = "playlist_items_list callable required"
                raise RuntimeError(msg)
            ledger["playlist_items_list_calls"] += 1
            return playlist_items_list(**params)
        if method == "videos.list":
            if videos_list is None:
                msg = "videos_list callable required"
                raise RuntimeError(msg)
            ledger["videos_list_calls"] += 1
            return videos_list(**params)
        msg = f"unsupported YouTube API method {method!r}"
        raise ValueError(msg)

    return fetch


def _channel_items(payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    items = payload.get("items", ())
    if isinstance(items, Mapping):
        return []
    return [item for item in items if isinstance(item, Mapping)]


def _subscriber_count(item: Mapping[str, Any]) -> int | None:
    statistics = item.get("statistics")
    if not isinstance(statistics, Mapping):
        return None
    if statistics.get("hiddenSubscriberCount") in (True, "true", "True", 1):
        return None
    return _parse_count(statistics.get("subscriberCount"))


def _channel_name(item: Mapping[str, Any]) -> str:
    snippet = item.get("snippet")
    if isinstance(snippet, Mapping):
        title = snippet.get("title")
        if isinstance(title, str) and title.strip():
            return title.strip()
    channel_id = item.get("id")
    if isinstance(channel_id, str):
        return channel_id
    return "unknown"


def _topic_ids(item: Mapping[str, Any]) -> tuple[str, ...]:
    topic = item.get("topicDetails")
    if not isinstance(topic, Mapping):
        return ()
    ids = topic.get("topicIds")
    if not isinstance(ids, Sequence) or isinstance(ids, (str, bytes)):
        return ()
    return tuple(str(topic_id) for topic_id in ids)


def _snippet_text(item: Mapping[str, Any]) -> tuple[str, str]:
    snippet = item.get("snippet")
    if not isinstance(snippet, Mapping):
        return "", ""
    title = snippet.get("title")
    description = snippet.get("description")
    return (
        str(title) if title is not None else "",
        str(description) if description is not None else "",
    )


def _coerce_search_result(raw: Mapping[str, object]) -> tuple[str, int | None]:
    channel_id = str(raw.get("channel_id", raw.get("channelId", ""))).strip()
    count = _parse_count(raw.get("subscriber_count", raw.get("subscriberCount")))
    return channel_id, count


@dataclass
class WatchlistManager:
    """In-memory watchlist with injected YouTube API callables (offline-safe)."""

    now_ms: int
    channels_list: ChannelsList
    playlist_items_list: PlaylistItemsList | None = None
    videos_list: VideosList | None = None
    _channels: dict[str, WatchlistChannel] = field(default_factory=dict)
    _ledger: MutableMapping[str, int] = field(
        default_factory=lambda: {
            "search_list_calls": 0,
            "channels_list_calls": 0,
            "playlist_items_list_calls": 0,
            "videos_list_calls": 0,
        }
    )

    def active_count(self) -> int:
        return sum(1 for row in self._channels.values() if row.is_active)

    def snapshot(self) -> tuple[WatchlistChannel, ...]:
        return tuple(self._channels[ch_id] for ch_id in sorted(self._channels))

    def known_channel_ids(self) -> frozenset[str]:
        return frozenset(self._channels)

    def _ledger_snapshot(self) -> ApiCallLedger:
        return ApiCallLedger(
            search_list_calls=self._ledger["search_list_calls"],
            channels_list_calls=self._ledger["channels_list_calls"],
            playlist_items_list_calls=self._ledger["playlist_items_list_calls"],
            videos_list_calls=self._ledger["videos_list_calls"],
        )

    def _youtube(self) -> Callable[[str], Mapping[str, Any]]:
        return _guard_youtube(
            channels_list=self.channels_list,
            playlist_items_list=self.playlist_items_list,
            videos_list=self.videos_list,
            ledger=self._ledger,
        )

    def _in_subscriber_band(self, count: int | None) -> bool:
        return count is not None and SUBSCRIBER_COUNT_MIN <= count <= SUBSCRIBER_COUNT_MAX

    def _room_for_spillover(self) -> bool:
        return self.active_count() < TARGET_ACTIVE_MAX

    def seed(self, channel_ids: Sequence[str]) -> SeedResult:
        """Bulk-seed via ``channels.list`` only (50 ids per call, zero ``search.list``)."""
        fetch = self._youtube()
        unique = list(dict.fromkeys(channel_ids))
        admitted: list[WatchlistChannel] = []
        rejected_band: list[str] = []

        for batch in _batched(unique, CHANNELS_LIST_BATCH_SIZE):
            payload = fetch(
                "channels.list",
                part="snippet,statistics,contentDetails,topicDetails",
                id=",".join(batch),
            )
            for item in _channel_items(payload):
                channel_id = str(item.get("id", ""))
                if not channel_id or channel_id in self._channels:
                    continue
                subs = _subscriber_count(item)
                if not self._in_subscriber_band(subs):
                    rejected_band.append(channel_id)
                    continue
                title, description = _snippet_text(item)
                if not topic_matches_true_crime(
                    title=title,
                    description=description,
                    topic_ids=_topic_ids(item),
                ):
                    rejected_band.append(channel_id)
                    continue
                uploads = channel_to_uploads_playlist_id(channel_id)
                row = WatchlistChannel(
                    channel_id=channel_id,
                    uploads_playlist_id=uploads,
                    channel_name=_channel_name(item),
                    subscriber_count=int(subs),
                    yt_ttl_expires_at=self.now_ms + YT_TTL_MS,
                    discovered_via=DISCOVERED_VIA_SEED,
                    last_upload_at_ms=self.now_ms,
                )
                self._channels[channel_id] = row
                admitted.append(row)

        return SeedResult(
            admitted=tuple(admitted),
            rejected_band=tuple(rejected_band),
            ledger=self._ledger_snapshot(),
        )

    def discover_spillover_channels(
        self,
        search_results: Sequence[Mapping[str, object]],
    ) -> SpilloverDiscoveryResult:
        """Promote spillover channels that pass band, topic, and long-form crime checks."""
        if not search_results:
            return SpilloverDiscoveryResult(
                promoted=(),
                rejected=(),
                ledger=self._ledger_snapshot(),
            )
        if not self._room_for_spillover():
            return SpilloverDiscoveryResult(
                promoted=(),
                rejected=tuple(_coerce_search_result(r)[0] for r in search_results if _coerce_search_result(r)[0]),
                ledger=self._ledger_snapshot(),
            )
        if self.playlist_items_list is None or self.videos_list is None:
            msg = "playlist_items_list and videos_list are required for spillover discovery"
            raise RuntimeError(msg)

        fetch = self._youtube()
        promoted: list[WatchlistChannel] = []
        rejected: list[str] = []

        unknown: list[str] = []
        for raw in search_results:
            channel_id, pre_count = _coerce_search_result(raw)
            if not channel_id or channel_id in self._channels:
                continue
            if pre_count is not None and not self._in_subscriber_band(pre_count):
                rejected.append(channel_id)
                continue
            unknown.append(channel_id)

        if not unknown:
            return SpilloverDiscoveryResult(
                promoted=(),
                rejected=tuple(rejected),
                ledger=self._ledger_snapshot(),
            )

        channel_meta: dict[str, Mapping[str, Any]] = {}
        for batch in _batched(unknown, CHANNELS_LIST_BATCH_SIZE):
            payload = fetch(
                "channels.list",
                part="snippet,statistics,topicDetails",
                id=",".join(batch),
            )
            for item in _channel_items(payload):
                channel_id = str(item.get("id", ""))
                if channel_id:
                    channel_meta[channel_id] = item

        for channel_id in unknown:
            if not self._room_for_spillover():
                rejected.append(channel_id)
                continue
            item = channel_meta.get(channel_id)
            if item is None:
                rejected.append(channel_id)
                continue
            subs = _subscriber_count(item)
            if not self._in_subscriber_band(subs):
                rejected.append(channel_id)
                continue
            title, description = _snippet_text(item)
            if not topic_matches_true_crime(
                title=title,
                description=description,
                topic_ids=_topic_ids(item),
            ):
                rejected.append(channel_id)
                continue
            crime_long = self._count_crime_long_form_uploads(fetch, channel_id)
            if crime_long < MIN_CRIME_LONG_FORM_IN_LAST_10:
                rejected.append(channel_id)
                continue
            row = WatchlistChannel(
                channel_id=channel_id,
                uploads_playlist_id=channel_to_uploads_playlist_id(channel_id),
                channel_name=_channel_name(item),
                subscriber_count=int(subs),
                yt_ttl_expires_at=self.now_ms + YT_TTL_MS,
                discovered_via=DISCOVERED_VIA_SPILLOVER,
                last_upload_at_ms=self.now_ms,
            )
            self._channels[channel_id] = row
            promoted.append(row)

        return SpilloverDiscoveryResult(
            promoted=tuple(promoted),
            rejected=tuple(rejected),
            ledger=self._ledger_snapshot(),
        )

    def _count_crime_long_form_uploads(
        self,
        fetch: Callable[[str], Mapping[str, Any]],
        channel_id: str,
    ) -> int:
        playlist_id = channel_to_uploads_playlist_id(channel_id)
        page = fetch(
            "playlistItems.list",
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=PLAYLIST_ITEMS_PAGE_SIZE,
        )
        video_ids: list[str] = []
        for item in _channel_items(page):
            details = item.get("contentDetails")
            if isinstance(details, Mapping):
                video_id = details.get("videoId")
                if isinstance(video_id, str) and video_id:
                    video_ids.append(video_id)
        if not video_ids:
            return 0

        crime_count = 0
        for batch in _batched(video_ids, VIDEOS_LIST_BATCH_SIZE):
            payload = fetch(
                "videos.list",
                part="snippet,contentDetails",
                id=",".join(batch),
            )
            for item in _channel_items(payload):
                snippet = item.get("snippet")
                content = item.get("contentDetails")
                if not isinstance(snippet, Mapping) or not isinstance(content, Mapping):
                    continue
                title = str(snippet.get("title", ""))
                description = str(snippet.get("description", ""))
                duration_raw = content.get("duration")
                if not isinstance(duration_raw, str):
                    continue
                try:
                    duration_sec = parse_iso8601_duration(duration_raw)
                except ValueError:
                    continue
                if not is_long_form(
                    duration_sec=duration_sec,
                    title=title,
                    description=description,
                ):
                    continue
                if title_looks_like_crime_video(title, description):
                    crime_count += 1
        return crime_count

    def prune(self, now_ms: int | None = None) -> PruneResult:
        """Deactivate dormant channels (>180d since last upload) and graduated (>120K subs)."""
        effective_now = self.now_ms if now_ms is None else now_ms
        fetch = self._youtube()
        dormant: list[str] = []
        graduated: list[str] = []

        active_ids = [
            channel_id
            for channel_id, row in self._channels.items()
            if row.is_active
        ]
        refreshed: dict[str, tuple[int, int]] = {}
        for batch in _batched(active_ids, CHANNELS_LIST_BATCH_SIZE):
            payload = fetch(
                "channels.list",
                part="statistics",
                id=",".join(batch),
            )
            for item in _channel_items(payload):
                channel_id = str(item.get("id", ""))
                subs = _subscriber_count(item)
                if channel_id and subs is not None:
                    refreshed[channel_id] = (subs, self._channels[channel_id].last_upload_at_ms)

        for channel_id, row in list(self._channels.items()):
            if not row.is_active:
                continue
            subs, last_upload = refreshed.get(channel_id, (row.subscriber_count, row.last_upload_at_ms))
            if subs > SUBSCRIBER_COUNT_MAX:
                self._channels[channel_id] = replace(
                    row,
                    is_active=False,
                    subscriber_count=subs,
                )
                graduated.append(channel_id)
                continue
            if effective_now - last_upload > DORMANT_MS:
                self._channels[channel_id] = replace(row, is_active=False)
                dormant.append(channel_id)

        return PruneResult(
            dormant_deactivated=tuple(dormant),
            graduated_deactivated=tuple(graduated),
            ledger=self._ledger_snapshot(),
        )