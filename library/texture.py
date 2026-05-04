from . import primitives

def scanline_texture(surface, points, uvs, texture, transparent_color=None):
    """
    Renderiza um polígono texturizado usando o algoritmo Scanline.
    Inclui otimização incremental (DDA) para cálculo de U/V e suporte a Color Keying.
    """
    tex_w, tex_h = texture.get_width(), texture.get_height()
    n = len(points)
    ys = [p[1] for p in points]
    y_min = int(min(ys))
    y_max = int(max(ys))

    for y in range(y_min, y_max):
        inter = []
        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]

            u0, v0 = uvs[i]
            u1, v1 = uvs[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                u0, v0, u1, v1 = u1, v1, u0, v0

            if y < y0 or y >= y1:
                continue

            t = (y - y0) / (y1 - y0)

            x = x0 + t * (x1 - x0)
            u = u0 + t * (u1 - u0)
            v = v0 + t * (v1 - v0)

            inter.append((x, u, v))

        inter.sort(key=lambda item: item[0])

        for i in range(0, len(inter), 2):
            if i + 1 >= len(inter):
                continue

            x_start, u_start, v_start = inter[i]
            x_end,   u_end,   v_end   = inter[i + 1]

            width = x_end - x_start
            if width <= 0:
                continue

            # --- OTIMIZAÇÃO: DIFERENÇAS INCREMENTAIS ---
            du = (u_end - u_start) / width
            dv = (v_end - v_start) / width

            # Ajuste de sub-píxel
            x_int_start = int(x_start)
            offset = x_int_start - x_start
            curr_u = u_start + (offset * du)
            curr_v = v_start + (offset * dv)

            for x in range(x_int_start, int(x_end) + 1):
                tx = int(curr_u * (tex_w - 1))
                ty = int(curr_v * (tex_h - 1))

                if 0 <= tx < tex_w and 0 <= ty < tex_h:
                    color = texture.get_at((tx, ty))

                    if transparent_color is not None:
                        tr, tg, tb = transparent_color
                        r, g, b = color[0], color[1], color[2]
                        if abs(r - tr) > 15 or abs(g - tg) > 15 or abs(b - tb) > 15:
                            primitives.set_pixel(surface, x, y, color)
                    else:
                        primitives.set_pixel(surface, x, y, color)

                # Avança U e V para o próximo píxel de X por adição
                curr_u += du
                curr_v += dv
