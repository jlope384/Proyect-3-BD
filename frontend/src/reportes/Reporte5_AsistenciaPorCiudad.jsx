import { useState, useEffect } from 'react';
import { getAsistenciaPorCiudad, getCiudades } from '../api/reportesService';
import FiltrosReporte from '../components/FiltrosReporte';
import GraficaBarras from '../components/GraficaBarras';
import TablaResultados from '../components/TablaResultados';
import { utils as xlsxUtils, writeFile as xlsxWriteFile } from 'xlsx';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

export default function ReporteAsistenciaPorCiudad() {
  const [datos, setDatos] = useState([]);
  const [ciudades, setCiudades] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [filtros, setFiltros] = useState({
    fecha_inicio: '',
    fecha_fin: '',
    ciudad_id: '',
    pais: '',
    min_asistentes: 0,
    skip: 0,
    limit: 10
  });

  // Exportar a Excel
  const exportToExcel = () => {
    const datosExportar = datos.map(item => ({
      'Ciudad': item.ciudad,
      'País': item.pais,
      'Asistentes Únicos': item.asistentes_unicos,
      'Total Asistencias': item.total_asistencias,
      'Eventos Realizados': item.total_eventos
    }));

    const worksheet = xlsxUtils.json_to_sheet(datosExportar);
    const workbook = xlsxUtils.book_new();
    xlsxUtils.book_append_sheet(workbook, worksheet, "AsistenciaPorCiudad");
    xlsxWriteFile(workbook, "Asistencia_Por_Ciudad.xlsx");
  };

  // Exportar a PDF
  const exportToPDF = () => {
    const doc = new jsPDF();
    doc.text("Reporte de Asistencia por Ciudad", 14, 15);
    doc.autoTable({
      head: [['Ciudad', 'País', 'Asistentes Únicos', 'Total Asistencias', 'Eventos']],
      body: datos.map(item => [
        item.ciudad,
        item.pais,
        item.asistentes_unicos,
        item.total_asistencias,
        item.total_eventos
      ]),
      startY: 20,
      styles: { fontSize: 8 },
      headStyles: { fillColor: [76, 175, 80] }
    });
    doc.save("Asistencia_Por_Ciudad.pdf");
  };

  // Cargar opciones de filtros (ciudades)
  useEffect(() => {
    const cargarOpciones = async () => {
      try {
        const [resCiudades] = await Promise.all([
          getCiudades()
        ]);
        setCiudades(resCiudades.data);
      } catch (error) {
        console.error("Error cargando opciones:", error);
        setError("Error al cargar opciones de filtros");
      }
    };
    cargarOpciones();
  }, []);

  // Cargar datos del reporte
  useEffect(() => {
    const cargarDatos = async () => {
      if (!filtros.fecha_inicio || !filtros.fecha_fin) return;

      setLoading(true);
      setError(null);
      try {
        const { data } = await getAsistenciaPorCiudad(filtros);
        setDatos(data || []);
      } catch (error) {
        console.error("Error cargando datos:", error);
        setError("Error al cargar datos. Verifica la conexión.");
      } finally {
        setLoading(false);
      }
    };
    cargarDatos();
  }, [filtros]);

  return (
    <div className="reporte-container">
      <div className="reporte-header">
        <h2>Asistencia por Ciudad</h2>
        <div className="export-buttons">
          <button onClick={exportToExcel} className="export-btn excel">
            Exportar a Excel
          </button>
          <button onClick={exportToPDF} className="export-btn pdf">
            Exportar a PDF
          </button>
        </div>
      </div>

      <FiltrosReporte
        filtros={filtros}
        onChange={(nuevosFiltros) => setFiltros({ ...nuevosFiltros, skip: 0 })}
        campos={[
          {
            tipo: 'fecha',
            nombre: 'fecha_inicio',
            etiqueta: 'Fecha Inicio',
            requerido: true
          },
          {
            tipo: 'fecha',
            nombre: 'fecha_fin',
            etiqueta: 'Fecha Fin',
            requerido: true
          },
          {
            tipo: 'select',
            nombre: 'ciudad_id',
            etiqueta: 'Ciudad',
            opciones: ciudades.map(c => ({ id: c.id, nombre: c.nombre })),
            opcionVacia: "Todas las ciudades"
          },
          {
            tipo: 'text',
            nombre: 'pais',
            etiqueta: 'País',
            placeholder: 'Filtrar por país'
          },
          {
            tipo: 'number',
            nombre: 'min_asistentes',
            etiqueta: 'Mín. Asistentes',
            min: 0,
            step: 10
          }
        ]}
      />

      {loading ? (
        <div className="loading">Cargando datos...</div>
      ) : error ? (
        <div className="error">{error}</div>
      ) : datos.length === 0 ? (
        <div className="no-data">No hay datos con los filtros seleccionados</div>
      ) : (
        <>
          <div className="visualizacion">
            <GraficaBarras
              datos={datos.map(item => ({
                label: `${item.ciudad} (${item.pais})`,
                value: item.total_asistencias
              }))}
              titulo="Total Asistencias por Ciudad"
            />
            
            <TablaResultados
              datos={datos}
              columnas={[
                { key: 'ciudad', titulo: 'Ciudad' },
                { key: 'pais', titulo: 'País' },
                { key: 'asistentes_unicos', titulo: 'Asistentes Únicos' },
                { key: 'total_asistencias', titulo: 'Total Asistencias' },
                { key: 'total_eventos', titulo: 'Eventos Realizados' }
              ]}
            />
          </div>

          <div className="paginacion">
            <button 
              disabled={filtros.skip === 0}
              onClick={() => setFiltros({ ...filtros, skip: Math.max(0, filtros.skip - filtros.limit) })}
            >
              Anterior
            </button>
            <span>Página {Math.floor(filtros.skip / filtros.limit) + 1}</span>
            <button 
              disabled={datos.length < filtros.limit}
              onClick={() => setFiltros({ ...filtros, skip: filtros.skip + filtros.limit })}
            >
              Siguiente
            </button>
          </div>
        </>
      )}
    </div>
  );
}