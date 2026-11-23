/** Deterministic 10x10 cell to pixel and zoom. Mirrors the Python helper. No I/O. */

export interface GridCellZoom {
  grid_cell: string;
  col_index: number;
  row_index: number;
  x_px: number;
  y_px: number;
  span_cols: number;
  span_rows: number;
  zoom_x: number;
  zoom_y: number;
  target_zoom: number;
  width_px: number;
  height_px: number;
}

const CELL = /^([A-J])([1-9]|10)$/;

function roundDiv(numer: number, denom: number): number {
  return Math.floor((numer + Math.floor(denom / 2)) / denom);
}

function quantize4(value: number): number {
  return Math.round(value * 10000) / 10000;
}

export function gridCellToPixelAndZoom(args: {
  grid_cell: string;
  span_cols?: number;
  span_rows?: number;
  width_px?: number;
  height_px?: number;
}): GridCellZoom {
  const spanCols = args.span_cols ?? 1;
  const spanRows = args.span_rows ?? 1;
  const widthPx = args.width_px ?? 2560;
  const heightPx = args.height_px ?? 1440;
  const match = CELL.exec(args.grid_cell);
  if (!match) throw new Error("grid_cell must match [A-J][1-9] or [A-J]10");
  if (!Number.isInteger(widthPx) || !Number.isInteger(heightPx) || widthPx <= 0 || heightPx <= 0) {
    throw new Error("plate dimensions must be positive integers");
  }
  if (!(spanCols > 0 && spanCols <= 10) || !(spanRows > 0 && spanRows <= 10)) {
    throw new Error("span_cols and span_rows must be within (0, 10]");
  }
  const colIndex = match[1].charCodeAt(0) - "A".charCodeAt(0);
  const rowIndex = Number(match[2]) - 1;
  const zoomX = quantize4(8 / spanCols);
  const zoomY = quantize4(8 / spanRows);
  let target = Math.min(zoomX, zoomY);
  target = Math.min(3.8, Math.max(1.6, target));
  return {
    grid_cell: args.grid_cell,
    col_index: colIndex,
    row_index: rowIndex,
    x_px: roundDiv((2 * colIndex + 1) * widthPx, 20),
    y_px: roundDiv((2 * rowIndex + 1) * heightPx, 20),
    span_cols: spanCols,
    span_rows: spanRows,
    zoom_x: zoomX,
    zoom_y: zoomY,
    target_zoom: quantize4(target),
    width_px: widthPx,
    height_px: heightPx,
  };
}
