from fastapi import APIRouter, Query, HTTPException
from database import get_connection
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/reportes")

def validar_fechas(fecha_inicio: Optional[str], fecha_fin: Optional[str]):
    if fecha_inicio and fecha_fin:
        try:
            fecha_ini = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
            if fecha_ini > fecha_fin:
                raise HTTPException(
                    status_code=400,
                    detail="La fecha de inicio no puede ser mayor a la fecha fin"
                )
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Formato de fecha inválido. Use YYYY-MM-DD"
            )

# Reporte 1: Asistencia por Evento
@router.get(
    "/asistencia-evento",
    summary="Reporte de asistencia por evento",
    description="""Muestra la cantidad de asistentes por evento con filtros por:
    - Rango de fechas
    - Ciudad
    - Categoría de evento"""
)
def reporte_asistencia(
    fecha_inicio: Optional[str] = Query(
        None,
        description="Fecha de inicio en formato YYYY-MM-DD"
    ),
    fecha_fin: Optional[str] = Query(
        None, 
        description="Fecha fin en formato YYYY-MM-DD"
    ),
    ciudad_id: Optional[int] = Query(
        None,
        description="ID de la ciudad para filtrar"
    ),
    categoria_id: Optional[int] = Query(
        None,
        description="ID de la categoría de evento"
    ),
    skip: int = Query(
        0,
        description="Número de registros a omitir (paginación)"
    ),
    limit: int = Query(
        100,
        description="Límite de registros por página",
        le=200  # Máximo 200 registros por página
    )
):
    validar_fechas(fecha_inicio, fecha_fin)
    
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                e.id,
                e.nombre AS evento,
                COUNT(ra.id_asistente) AS asistentes,
                c.nombre AS categoria,
                l.nombre AS lugar,
                ci.nombre AS ciudad
            FROM evento e
            LEFT JOIN registro_asistencia ra ON e.id = ra.id_evento
            JOIN categoria_evento c ON e.id_categoria_evento = c.id
            JOIN lugar l ON e.id_lugar = l.id
            JOIN ciudad ci ON l.id_ciudad = ci.id
            WHERE 1=1
        """
        params = []
        
        if fecha_inicio:
            query += " AND e.fecha >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND e.fecha <= %s"
            params.append(fecha_fin)
        if ciudad_id:
            query += " AND l.id_ciudad = %s"
            params.append(ciudad_id)
        if categoria_id:
            query += " AND e.id_categoria_evento = %s"
            params.append(categoria_id)

        query += """
            GROUP BY e.id, e.nombre, c.nombre, l.nombre, ci.nombre
            ORDER BY asistentes DESC
            LIMIT %s OFFSET %s
        """
        params.extend([limit, skip])
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        
        # Consulta para total de registros (sin paginación)
        cursor.execute("SELECT COUNT(*) FROM (" + query.replace("LIMIT %s OFFSET %s", "") + ") AS subquery", params[:-2])
        total = cursor.fetchone()[0]
        
        return {
            "data": resultados,
            "paginacion": {
                "total": total,
                "skip": skip,
                "limit": limit
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el servidor: {str(e)}"
        )
    finally:
        if conn:
            conn.close()

# Reporte 2: Ventas Totales
@router.get(
    "/ventas-totales",
    summary="Reporte de ventas totales",
    description="""Métricas de ventas con filtros por:
    - Rango de fechas
    - Tipo de entrada
    - Medio de pago"""
)
def reporte_ventas(
    fecha_inicio: Optional[str] = Query(None),
    fecha_fin: Optional[str] = Query(None),
    tipo_entrada_id: Optional[int] = Query(None),
    medio_pago_id: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 100
):
    validar_fechas(fecha_inicio, fecha_fin)
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                e.nombre AS evento,
                te.descripcion AS tipo_entrada,
                mp.metodo AS medio_pago,
                COUNT(en.id) AS cantidad,
                SUM(en.precio_final) AS total,
                AVG(en.precio_final) AS promedio_venta
            FROM entrada en
            JOIN evento e ON en.id_evento = e.id
            JOIN tipo_entrada te ON en.id_tipo_entrada = te.id
            JOIN medio_pago mp ON en.id_medio_pago = mp.id
            WHERE 1=1
        """
        params = []

        if fecha_inicio:
            query += " AND e.fecha >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND e.fecha <= %s"
            params.append(fecha_fin)
        if tipo_entrada_id:
            query += " AND te.id = %s"
            params.append(tipo_entrada_id)
        if medio_pago_id:
            query += " AND mp.id = %s"
            params.append(medio_pago_id)

        query += """
            GROUP BY e.nombre, te.descripcion, mp.metodo
            ORDER BY total DESC
            LIMIT %s OFFSET %s
        """
        params.extend([limit, skip])
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        
        return {
            "data": resultados,
            "moneda": "GTQ",
            "paginacion": {
                "skip": skip,
                "limit": limit
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar reporte: {str(e)}"
        )
    finally:
        if conn:
            conn.close()

# Reporte 3: Artistas Populares
@router.get(
    "/artistas-populares",
    summary="Reporte de artistas más populares",
    response_description="Lista de artistas ordenados por asistencia"
)
def reporte_artistas(
    fecha_inicio: Optional[str] = Query(None),
    fecha_fin: Optional[str] = Query(None),
    tipo_artista: Optional[str] = Query(None),
    min_eventos: int = Query(1, description="Mínimo de eventos participados")
):
    validar_fechas(fecha_inicio, fecha_fin)
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                a.id,
                a.nombre AS artista,
                a.tipo,
                COUNT(DISTINCT ea.id_evento) AS eventos_participados,
                COUNT(DISTINCT ra.id_asistente) AS asistentes_totales,
                COUNT(ra.id) AS total_asistencias
            FROM artista a
            JOIN evento_artista ea ON a.id = ea.id_artista
            JOIN evento e ON ea.id_evento = e.id
            LEFT JOIN registro_asistencia ra ON e.id = ra.id_evento
            WHERE 1=1
        """
        params = []

        if fecha_inicio:
            query += " AND e.fecha >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND e.fecha <= %s"
            params.append(fecha_fin)
        if tipo_artista:
            query += " AND a.tipo = %s"
            params.append(tipo_artista)
            
        query += """
            GROUP BY a.id, a.nombre, a.tipo
            HAVING COUNT(DISTINCT ea.id_evento) >= %s
            ORDER BY asistentes_totales DESC
        """
        params.append(min_eventos)
        
        cursor.execute(query, params)
        return cursor.fetchall()
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar artistas: {str(e)}"
        )
    finally:
        if conn:
            conn.close()

# Reporte 4: Eventos por Categoría
@router.get("/eventos-por-categoria")
def reporte_categorias(
    fecha_inicio: Optional[str] = Query(None),
    fecha_fin: Optional[str] = Query(None),
    ingresos_minimos: float = Query(0, description="Filtrar por ingresos mínimos")
):
    validar_fechas(fecha_inicio, fecha_fin)
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            WITH eventos_con_ingresos AS (
                SELECT 
                    e.id,
                    e.id_categoria_evento,
                    COALESCE(SUM(en.precio_final), 0) AS ingresos_totales
                FROM evento e
                LEFT JOIN entrada en ON e.id = en.id_evento
                WHERE 1=1
        """
        params = []

        if fecha_inicio:
            query += " AND e.fecha >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND e.fecha <= %s"
            params.append(fecha_fin)
            
        query += """
                GROUP BY e.id, e.id_categoria_evento
            )
            SELECT 
                c.id,
                c.nombre AS categoria,
                COUNT(eci.id) AS total_eventos,
                SUM(eci.ingresos_totales) AS ingresos_totales,
                AVG(eci.ingresos_totales) AS promedio_ingresos
            FROM categoria_evento c
            LEFT JOIN eventos_con_ingresos eci ON c.id = eci.id_categoria_evento
            GROUP BY c.id, c.nombre
            HAVING SUM(eci.ingresos_totales) >= %s
            ORDER BY total_eventos DESC
        """
        params.append(ingresos_minimos)
        
        cursor.execute(query, params)
        return cursor.fetchall()
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar reporte: {str(e)}"
        )
    finally:
        if conn:
            conn.close()

# Reporte 5: Asistencia por Ciudad
@router.get("/asistencia-por-ciudad")
def reporte_ciudades(
    fecha_inicio: Optional[str] = Query(None),
    fecha_fin: Optional[str] = Query(None),
    pais: Optional[str] = Query(None, description="Filtrar por país")
):
    validar_fechas(fecha_inicio, fecha_fin)
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                ci.id,
                ci.nombre AS ciudad,
                ci.pais,
                COUNT(DISTINCT ra.id_asistente) AS asistentes_unicos,
                COUNT(ra.id) AS total_asistencias,
                COUNT(DISTINCT e.id) AS total_eventos
            FROM ciudad ci
            JOIN lugar l ON ci.id = l.id_ciudad
            JOIN evento e ON l.id = e.id_lugar
            LEFT JOIN registro_asistencia ra ON e.id = ra.id_evento
            WHERE 1=1
        """
        params = []

        if fecha_inicio:
            query += " AND e.fecha >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND e.fecha <= %s"
            params.append(fecha_fin)
        if pais:
            query += " AND ci.pais ILIKE %s"
            params.append(f"%{pais}%")
            
        query += """
            GROUP BY ci.id, ci.nombre, ci.pais
            ORDER BY total_asistencias DESC
        """
        
        cursor.execute(query, params)
        return cursor.fetchall()
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar ciudades: {str(e)}"
        )
    finally:
        if conn:
            conn.close()