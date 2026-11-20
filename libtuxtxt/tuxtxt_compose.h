/******************************************************************************
 * tuxtxt_compose.h - rendering of accented characters                        *
 *                                                                            *
 * - tuxtxt_merge_sbit():     position-correct merge of base and accent glyph *
 * - tuxtxt_get_accent(), tuxtxt_make_accent(), tuxtxt_lower_accent():        *
 *                            accent glyphs for the small bitmap strikes of   *
 *                            tuxtxt.otb, where some accents are blank        *
 ******************************************************************************/
#ifndef TUXTXT_COMPOSE_H
#define TUXTXT_COMPOSE_H

#include <stdlib.h>
#include <string.h>

#if ((defined(FREETYPE_MAJOR)) && (((FREETYPE_MAJOR == 2) && (((FREETYPE_MINOR == 1) && (FREETYPE_PATCH >= 9)) || (FREETYPE_MINOR > 1))) || (FREETYPE_MAJOR > 2)))
#define TUXTXT_SBIT_LOOKUP(ri, g, out) FTC_SBitCache_Lookup((ri)->cache, &(ri)->typettf, (g), (out), NULL)
#else
#define TUXTXT_SBIT_LOOKUP(ri, g, out) FTC_SBit_Cache_Lookup((ri)->cache, &(ri)->typettf, (g), (out))
#endif

/* The Latin G2 set asks for the combining marks U+0300, U+0301 and U+0303 and for U+02C9. They are missing in
 * tuxtxt.ttf, and blank bitmaps in the 21/22 pixel strikes of tuxtxt.otb. The spacing characters below look
 * the same and are real glyphs in all strikes. */
static int tuxtxt_accent_substitute(int c)
{
	switch (c)
	{
	case 0x0300: return 0x0060; /* grave */
	case 0x0301: return 0x00B4; /* acute */
	case 0x0303: return 0x02DC; /* tilde */
	case 0x02C9: return 0x00AF; /* macron */
	}
	return c;
}

/* copy a 1 bpp glyph bitmap into a destination bitmap; (left, top) is the destination origin */
static void tuxtxt_blit_mono(unsigned char *dst, int dpitch, int dleft, int dtop, const FTC_SBitRec *src)
{
	int x, y;
	for (y = 0; y < src->height; y++)
	{
		int dy = dtop - (src->top - y);
		for (x = 0; x < src->width; x++)
			if (src->buffer[y * src->pitch + (x >> 3)] & (0x80 >> (x & 7)))
			{
				int dx = src->left + x - dleft;
				dst[dy * dpitch + (dx >> 3)] |= 0x80 >> (dx & 7);
			}
	}
}

/* Merge accent into base glyph using the real glyph positions (left/top).
 * The result covers the union of both bounding boxes, so an accent that sticks out
 * above the base glyph is kept. Returns a static glyph, or NULL if it can't be done. */
static FTC_SBit tuxtxt_merge_sbit(FTC_SBit base, const FTC_SBitRec *acc)
{
	static FTC_SBitRec m;
	static unsigned char buf[1000];
	int left, right, top, bottom, w, h, pitch;

	if (base->format != 1 || acc->format != 1) /* only 1 bpp (FT_PIXEL_MODE_MONO) */
		return NULL;
	left   = base->left < acc->left ? base->left : acc->left;
	right  = base->left + base->width > acc->left + acc->width ? base->left + base->width : acc->left + acc->width;
	top    = base->top > acc->top ? base->top : acc->top;
	bottom = base->top - base->height < acc->top - acc->height ? base->top - base->height : acc->top - acc->height;
	w = right - left;
	h = top - bottom;
	pitch = (w + 7) / 8;
	if (w <= 0 || h <= 0 || pitch * h > (int)sizeof(buf))
		return NULL;
	memset(buf, 0, pitch * h);
	tuxtxt_blit_mono(buf, pitch, left, top, base);
	tuxtxt_blit_mono(buf, pitch, left, top, acc);
	m = *base;
	m.left = (FT_Char)left;
	m.top = (FT_Char)top;
	m.width = (FT_Byte)w;
	m.height = (FT_Byte)h;
	m.pitch = (FT_Short)pitch;
	m.buffer = buf;
	return &m;
}

/* ---- accents in the small bitmap strikes of tuxtxt.otb --------------------------------------------------------
 * In the 21 and 22 pixel strikes several spacing accents (U+0301, U+02C6, U+02C7, U+02D8, U+02DA) are blank bitmaps;
 * the font draws accented capitals there only as complete precomposed glyphs. For merging we need a usable accent. */

/* ink bounding box in absolute glyph coordinates (x to the right, y up); returns the number of set pixels */
static int tuxtxt_sbit_ink(const FTC_SBitRec *s, int *x0, int *y0, int *x1, int *y1)
{
	int x, y, pop = 0, ax0 = 10000, ax1 = -10000, ay0 = 10000, ay1 = -10000;
	for (y = 0; y < s->height; y++)
		for (x = 0; x < s->width; x++)
			if (s->buffer[y * s->pitch + (x >> 3)] & (0x80 >> (x & 7)))
			{
				int ax = s->left + x, ay = s->top - y;
				pop++;
				if (ax < ax0) ax0 = ax;
				if (ax > ax1) ax1 = ax;
				if (ay < ay0) ay0 = ay;
				if (ay > ay1) ay1 = ay;
			}
	if (x0) *x0 = ax0;
	if (y0) *y0 = ay0;
	if (x1) *x1 = ax1;
	if (y1) *y1 = ay1;
	return pop;
}

/* load glyph for code point c into a private copy; returns 1 on success */
static int tuxtxt_get_accent(tstRenderInfo *ri, int c, FTC_SBitRec *out, unsigned char *buf, int bufsize)
{
	FTC_SBit s;
	FT_UInt g = FT_Get_Char_Index(ri->face, c);
	if (!g || TUXTXT_SBIT_LOOKUP(ri, g, &s) != 0 || s->pitch * s->height > bufsize)
		return 0;
	*out = *s;
	memcpy(buf, s->buffer, s->pitch * s->height);
	out->buffer = buf;
	return 1;
}

/* move an accent that floats more than "gap" rows above the base letter down, so that it sits directly on top of the base glyph's ink */
static void tuxtxt_lower_accent(FTC_SBitRec *a, const FTC_SBitRec *base, int gap)
{
	int ay0, by1;
	if (tuxtxt_sbit_ink(a, 0, &ay0, 0, 0) && tuxtxt_sbit_ink(base, 0, 0, 0, &by1) && ay0 > by1 + 1 + gap)
		a->top -= ay0 - (by1 + 1);
}

/* draw a 3 row accent mark (G2 accents circumflex, caron, breve, ring) centered over the base glyph */
static int tuxtxt_make_accent(FTC_SBitRec *a, unsigned char *buf, int acc, const FTC_SBitRec *base)
{
	static const char *circ[3]  = { "..#..", ".#.#.", "#...#" };
	static const char *caron[3] = { "#...#", ".#.#.", "..#.." };
	static const char *breve[3] = { ".....", "#...#", ".###." };
	static const char *ring[3]  = { ".#.", "#.#", ".#." };
	const char **pat;
	int pw, r, c, bx0, bx1, by1;

	switch (acc)
	{
	case 0x3: pat = circ;  pw = 5; break;
	case 0xF: pat = caron; pw = 5; break;
	case 0x6: pat = breve; pw = 5; break;
	case 0xA: pat = ring;  pw = 3; break;
	default: return 0;
	}
	if (!tuxtxt_sbit_ink(base, &bx0, 0, &bx1, &by1))
		return 0;
	for (r = 0; r < 3; r++)
	{
		buf[r] = 0;
		for (c = 0; c < pw; c++)
			if (pat[r][c] == '#')
				buf[r] |= 0x80 >> c;
	}
	a->width = pw;
	a->height = 3;
	a->left = (bx0 + bx1) / 2 - pw / 2;
	a->top = by1 + 3;           /* lowest row of the mark is directly above the base glyph */
	a->format = 1;
	a->max_grays = 0;
	a->pitch = 1;
	a->xadvance = a->yadvance = 0;
	a->buffer = buf;
	return 1;
}
#endif
