# backend/routes/reportes.py

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date
from database import get_connection

router = APIRouter()

def dict_fetchall(cursor):
    """
    Si el cursor ya devuelve dicts (RealDictCursor), los retorna
    directamente; si no, construye la lista de dicts a partir de cursor.description.
    """
    rows = cursor.fetchall()
    if rows and isinstance(rows[0], dict):
        return rows

    cols = [col[0] for col in cursor.description]
    return [dict(zip(cols, row)) for row in rows]


@router.get(
    "/ventas-totales",
    response_model=List[dict],
    summary="Total recaudado por evento",
)
def reporte_ventas_totales(
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    monto_minimo: Optional[float] = Query(None),
    monto_maximo: Optional[float] = Query(None),
):
    """
    Devuelve recaudación total (precio_final) por evento,
    con filtros de fecha de compra y rango de montos.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT
                e.id AS evento_id,
                e.nombre AS evento_nombre,
                -- CAST a float8 para que JSON lo envíe como número
                COALESCE(SUM(en.precio_final), 0)::float8 AS total_recaudado
            FROM evento e
            LEFT JOIN entrada en ON en.id_evento = e.id
            WHERE 1=1
        """
        params = []
        if fecha_inicio:
            sql += " AND en.fecha_compra::date >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            sql += " AND en.fecha_compra::date <= %s"
            params.append(fecha_fin)
        if monto_minimo is not None:
            sql += " AND en.precio_final >= %s"
            params.append(monto_minimo)
        if monto_maximo is not None:
            sql += " AND en.precio_final <= %s"
            params.append(monto_maximo)

        sql += " GROUP BY e.id, e.nombre ORDER BY total_recaudado DESC"
        cursor.execute(sql, tuple(params))
        data = dict_fetchall(cursor)
        cursor.close()
        conn.close()
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/ventas-totales",
    response_model=List[dict],
    summary="Total recaudado por evento",
)
def reporte_ventas_totales(
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    monto_minimo: Optional[float] = Query(None),
    monto_maximo: Optional[float] = Query(None),
):
    """
    Devuelve recaudación total (precio_final) por evento,
    con filtros de fecha de compra y rango de montos.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT
                e.id AS evento_id,
                e.nombre AS evento_nombre,
                COALESCE(SUM(en.precio_final), 0) AS total_recaudado
            FROM evento e
            LEFT JOIN entrada en ON en.id_evento = e.id
            WHERE 1=1
        """
        params = []
        if fecha_inicio:
            sql += " AND en.fecha_compra::date >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            sql += " AND en.fecha_compra::date <= %s"
            params.append(fecha_fin)
        if monto_minimo is not None:
            sql += " AND en.precio_final >= %s"
            params.append(monto_minimo)
        if monto_maximo is not None:
            sql += " AND en.precio_final <= %s"
            params.append(monto_maximo)
        sql += " GROUP BY e.id, e.nombre ORDER BY total_recaudado DESC"
        cursor.execute(sql, tuple(params))
        data = dict_fetchall(cursor)
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/artistas-populares",
    response_model=List[dict],
    summary="Artistas con más asistencia",
)
def reporte_artistas_populares(
    limite: int = Query(10, ge=1, le=100),
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    tipo_evento_id: Optional[int] = Query(None),
):
    """
    Devuelve artistas ordenados por la suma de asistentes en sus eventos,
    con filtros:
      - límite de resultados
      - rango de fechas de evento
      - tipo de evento
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT
                a.id AS artista_id,
                a.nombre AS artista_nombre,
                COUNT(ra.id_asistente) AS total_asistencia
            FROM artista a
            JOIN evento_artista ea ON ea.id_artista = a.id
            JOIN evento e ON e.id = ea.id_evento
            JOIN registro_asistencia ra ON ra.id_evento = e.id
            WHERE 1=1
        """
        params = []

        if fecha_inicio:
            sql += " AND e.fecha >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            sql += " AND e.fecha <= %s"
            params.append(fecha_fin)
        if tipo_evento_id:
            sql += " AND e.id_tipo_evento = %s"
            params.append(tipo_evento_id)

        sql += " GROUP BY a.id, a.nombre ORDER BY total_asistencia DESC LIMIT %s"
        params.append(limite)

        cursor.execute(sql, tuple(params))
        data = dict_fetchall(cursor)
        cursor.close()
        conn.close()
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/eventos-por-categoria",
    response_model=List[dict],
    summary="Número de eventos por categoría",
)
def reporte_eventos_por_categoria(
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    tipo_evento_id: Optional[int] = Query(None),
    ciudad_id: Optional[int] = Query(None),
):
    """
    Devuelve cuántos eventos hay en cada categoría,
    con filtros:
      - rango de fechas de evento
      - tipo de evento
      - ciudad del lugar del evento
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT
                ce.id AS categoria_id,
                ce.nombre AS categoria_nombre,
                COUNT(e.id) AS total_eventos
            FROM categoria_evento ce
            LEFT JOIN evento e ON e.id_categoria_evento = ce.id
            LEFT JOIN lugar l ON l.id = e.id_lugar
            WHERE 1=1
        """
        params = []

        if fecha_inicio:
            sql += " AND e.fecha >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            sql += " AND e.fecha <= %s"
            params.append(fecha_fin)
        if tipo_evento_id:
            sql += " AND e.id_tipo_evento = %s"
            params.append(tipo_evento_id)
        if ciudad_id:
            sql += " AND l.id_ciudad = %s"
            params.append(ciudad_id)

        sql += " GROUP BY ce.id, ce.nombre ORDER BY total_eventos DESC"
        cursor.execute(sql, tuple(params))
        data = dict_fetchall(cursor)
        cursor.close()
        conn.close()
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/asistencia-por-ciudad",
    response_model=List[dict],
    summary="Asistencia total por ciudad",
)
def reporte_asistencia_por_ciudad(
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    tipo_evento_id: Optional[int] = Query(None),
    categoria_evento_id: Optional[int] = Query(None),
):
    """
    Devuelve número de asistentes por ciudad,
    con filtros:
      - rango de fechas de asistencia
      - tipo de evento
      - categoría de evento
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT
                c.id AS ciudad_id,
                c.nombre AS ciudad_nombre,
                COUNT(ra.id_asistente) AS total_asistencia
            FROM ciudad c
            LEFT JOIN lugar l ON l.id_ciudad = c.id
            LEFT JOIN evento e ON e.id_lugar = l.id
            LEFT JOIN registro_asistencia ra ON ra.id_evento = e.id
            WHERE 1=1
        """
        params = []

        if fecha_inicio:
            sql += " AND ra.fecha_hora::date >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            sql += " AND ra.fecha_hora::date <= %s"
            params.append(fecha_fin)
        if tipo_evento_id:
            sql += " AND e.id_tipo_evento = %s"
            params.append(tipo_evento_id)
        if categoria_evento_id:
            sql += " AND e.id_categoria_evento = %s"
            params.append(categoria_evento_id)

        sql += " GROUP BY c.id, c.nombre ORDER BY total_asistencia DESC"
        cursor.execute(sql, tuple(params))
        data = dict_fetchall(cursor)
        cursor.close()
        conn.close()
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))