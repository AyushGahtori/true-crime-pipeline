"""Offline tests for WatchlistManager."""

from __future__ import annotations

from dataclasses import replace

import pytest

from agent1_scout.watchlist import (
    YT_TTL_MS,
    DORMANT_MS,
    MIN_CRIME_LONG_FORM_IN_LAST_10,
    SUBSCRIBER_COUNT_MAX,
    SUBSCRIBER_COUNT_MIN,
    SearchListForbiddenError,
    WatchlistManager,
    channel_to_uploads_playlist_id,
)

NOW_MS = 1_700_000_000_000


def _channel_item(
    channel_id: str,
    *,
    subs: int,
    title: str = "Cold Case Files",
    description: str = "True crime documentary channel",
    topic_ids: tuple[str, ...] = (),
    hidden_subs: bool = False,
) -> dict:
    stats: dict = {"hiddenSubscriberCount": hidden_subs}
    if not hidden_subs:
        stats["subscriberCount"] = str(subs)
    topic_block: dict = {}
    if topic_ids:
        topic_block["topicDetails"] = {"topicIds": list(topic_ids)}
    return {
        "id": channel_id,
        "snippet": {"title": title, "description": description},
        "statistics": stats,
        **topic_block,
    }


def test_uc_to_uu_mapping() -> None:
    assert channel_to_uploads_playlist_id("UCabc123") == "UUabc123"


def test_seed_uses_channels_list_only_batches_fifty() -> None:
    seed_ids = [f"UC{i:020d}" for i in range(51)]
    calls: list[list[str]] = []

    def channels_list(*, id: str, **_kwargs):  # noqa: A002
        batch = id.split(",")
        calls.append(batch)
        items = [
            _channel_item(cid, subs=10_000, topic_ids=("/m/0jm_",))
            for cid in batch
        ]
        return {"items": items}

    manager = WatchlistManager(now_ms=NOW_MS, channels_list=channels_list)
    result = manager.seed(seed_ids)

    assert result.ledger.search_list_calls == 0
    assert result.ledger.channels_list_calls == 2
    assert len(result.admitted) == 51
    assert len(calls[0]) == 50
    assert len(calls[1]) == 1
    row = result.admitted[0]
    assert row.uploads_playlist_id == channel_to_uploads_playlist_id(row.channel_id)
    assert row.discovered_via == "SEED"
    assert row.yt_ttl_expires_at == NOW_MS + YT_TTL_MS


def test_seed_rejects_subscriber_band_edges() -> None:
    def channels_list(*, id: str, **_kwargs):  # noqa: A002
        items = [
            _channel_item("UC_low", subs=SUBSCRIBER_COUNT_MIN - 1),
            _channel_item("UC_ok", subs=SUBSCRIBER_COUNT_MIN),
            _channel_item("UC_high", subs=SUBSCRIBER_COUNT_MAX + 1),
        ]
        return {"items": items}

    manager = WatchlistManager(now_ms=NOW_MS, channels_list=channels_list)
    result = manager.seed(["UC_low", "UC_ok", "UC_high"])

    assert [c.channel_id for c in result.admitted] == ["UC_ok"]
    assert set(result.rejected_band) == {"UC_low", "UC_high"}


def test_seed_rejects_pop_culture_topic() -> None:
    def channels_list(*, id: str, **_kwargs):  # noqa: A002
        return {
            "items": [
                _channel_item(
                    "UC_pop",
                    subs=50_000,
                    title="Celebrity gossip weekly",
                    description="Pop culture drama recap",
                )
            ]
        }

    manager = WatchlistManager(now_ms=NOW_MS, channels_list=channels_list)
    result = manager.seed(["UC_pop"])
    assert result.admitted == ()
    assert result.rejected_band == ("UC_pop",)


def test_seed_forbids_search_list() -> None:
    def channels_list(**_kwargs):
        return {"items": []}

    manager = WatchlistManager(now_ms=NOW_MS, channels_list=channels_list)
    with pytest.raises(SearchListForbiddenError):
        manager._youtube()("search.list", q="true crime")


def test_spillover_promotes_qualifying_channel() -> None:
    admitted_channel = _channel_item("UC_seed", subs=20_000, topic_ids=("/m/0jm_",))

    def channels_list(*, id: str, part: str, **_kwargs):  # noqa: A002
        ids = id.split(",")
        if "UC_spill" in ids:
            return {
                "items": [
                    _channel_item(
                        "UC_spill",
                        subs=25_000,
                        title="Unsolved Homicide Files",
                        description="Murder investigations",
                        topic_ids=("/m/0jm_",),
                    )
                ]
            }
        return {"items": [admitted_channel]}

    crime_titles = [
        "Murder on Route 9 documentary",
        "Cold case homicide special",
        "Serial killer investigation",
        "Missing person unsolved",
    ]

    def playlist_items_list(*, playlistId: str, **_kwargs):  # noqa: N803
        assert playlistId == "UU_spill"
        return {
            "items": [
                {"contentDetails": {"videoId": f"v{i}"}}
                for i in range(MIN_CRIME_LONG_FORM_IN_LAST_10)
            ]
        }

    def videos_list(*, id: str, **_kwargs):  # noqa: A002
        items = []
        for index, video_id in enumerate(id.split(",")):
            items.append(
                {
                    "id": video_id,
                    "snippet": {
                        "title": crime_titles[index],
                        "description": "true crime",
                    },
                    "contentDetails": {"duration": "PT15M"},
                }
            )
        return {"items": items}

    manager = WatchlistManager(
        now_ms=NOW_MS,
        channels_list=channels_list,
        playlist_items_list=playlist_items_list,
        videos_list=videos_list,
    )
    manager.seed(["UC_seed"])
    spill = manager.discover_spillover_channels(
        [{"channel_id": "UC_spill", "subscriber_count": 25_000}]
    )

    assert spill.ledger.search_list_calls == 0
    assert len(spill.promoted) == 1
    assert spill.promoted[0].discovered_via == "SPILLOVER"
    assert spill.promoted[0].uploads_playlist_id == "UU_spill"


def test_spillover_rejects_shorts_farm() -> None:
    def channels_list(*, id: str, **_kwargs):  # noqa: A002
        return {
            "items": [
                _channel_item(
                    "UC_shorts",
                    subs=30_000,
                    title="True crime shorts",
                    description="Murder stories",
                )
            ]
        }

    def playlist_items_list(*, playlistId: str, **_kwargs):  # noqa: N803, ARG001
        return {
            "items": [
                {"contentDetails": {"videoId": f"v{i}"}} for i in range(10)
            ]
        }

    def videos_list(*, id: str, **_kwargs):  # noqa: A002
        return {
            "items": [
                {
                    "id": vid,
                    "snippet": {"title": "Murder recap #Shorts", "description": ""},
                    "contentDetails": {"duration": "PT45S"},
                }
                for vid in id.split(",")
            ]
        }

    manager = WatchlistManager(
        now_ms=NOW_MS,
        channels_list=channels_list,
        playlist_items_list=playlist_items_list,
        videos_list=videos_list,
    )
    spill = manager.discover_spillover_channels([{"channel_id": "UC_shorts"}])
    assert spill.promoted == ()
    assert spill.rejected == ("UC_shorts",)


def test_spillover_rejects_insufficient_long_form_crime() -> None:
    def channels_list(*, id: str, **_kwargs):  # noqa: A002
        return {
            "items": [
                _channel_item(
                    "UC_mixed",
                    subs=15_000,
                    title="Crime commentary",
                    description="Homicide discussion",
                )
            ]
        }

    def playlist_items_list(*, playlistId: str, **_kwargs):  # noqa: N803, ARG001
        return {
            "items": [
                {"contentDetails": {"videoId": f"v{i}"}} for i in range(10)
            ]
        }

    def videos_list(*, id: str, **_kwargs):  # noqa: A002
        items = []
        for index, video_id in enumerate(id.split(",")):
            if index < 2:
                title = "Murder documentary special"
                duration = "PT20M"
            else:
                title = "Netflix drama recap"
                duration = "PT20M"
            items.append(
                {
                    "id": video_id,
                    "snippet": {"title": title, "description": ""},
                    "contentDetails": {"duration": duration},
                }
            )
        return {"items": items}

    manager = WatchlistManager(
        now_ms=NOW_MS,
        channels_list=channels_list,
        playlist_items_list=playlist_items_list,
        videos_list=videos_list,
    )
    spill = manager.discover_spillover_channels([{"channel_id": "UC_mixed"}])
    assert spill.promoted == ()
    assert spill.rejected == ("UC_mixed",)


def test_prune_dormant_and_graduated() -> None:
    dormant_upload_ms = NOW_MS - DORMANT_MS - 1
    seed_channels = {
        "UC_dormant": _channel_item("UC_dormant", subs=40_000),
        "UC_grad": _channel_item("UC_grad", subs=100_000),
        "UC_ok": _channel_item("UC_ok", subs=50_000),
    }
    prune_channels = {
        **seed_channels,
        "UC_grad": _channel_item("UC_grad", subs=SUBSCRIBER_COUNT_MAX + 50_000),
    }

    def channels_list(*, id: str, part: str = "", **_kwargs):  # noqa: A002
        table = seed_channels if "snippet" in part else prune_channels
        return {
            "items": [table[cid] for cid in id.split(",") if cid in table]
        }

    manager = WatchlistManager(now_ms=NOW_MS, channels_list=channels_list)
    manager.seed(["UC_dormant", "UC_grad", "UC_ok"])
    manager._channels["UC_dormant"] = replace(
        manager._channels["UC_dormant"],
        last_upload_at_ms=dormant_upload_ms,
    )

    result = manager.prune(NOW_MS)
    assert result.dormant_deactivated == ("UC_dormant",)
    assert result.graduated_deactivated == ("UC_grad",)
    assert manager._channels["UC_ok"].is_active
    assert not manager._channels["UC_dormant"].is_active
    assert not manager._channels["UC_grad"].is_active