import { useState, useEffect } from 'react';
import { getAsistenciaEvento, getCiudades, getCategorias } from '../api/reportesService';
import FiltrosReporte from '../components/FiltrosReporte';
import GraficaBarras from '../components/GraficaBarras';
import TablaResultados from '../components/TablaResultados';
import { utils as xlsxUtils, writeFile as xlsxWriteFile } from 'xlsx';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

export default function ReporteAsistenciaEvento() {
  const [datos, setDatos] = useState([]);
  const [ciudades, setCiudades] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [filtros, setFiltros] = useState({
    fecha_inicio: '',
    fecha_fin: '',
    ciudad_id: '',
    categoria_id: '',
    skip: 0,
    limit: 10
  });

  // Exportar a Excel
  const exportToExcel = () => {
    const datosExportar = datos.map(item => ({
      'Evento': item.evento,
      'Asistentes': item.asistentes,
      'Categoría': item.categoria,
      'Lugar': item.lugar,
      'Ciudad': item.ciudad
    }));

    const worksheet = xlsxUtils.json_to_sheet(datosExportar);
    const workbook = xlsxUtils.book_new();
    xlsxUtils.book_append_sheet(workbook, worksheet, "AsistenciaEventos");
    xlsxWriteFile(workbook, "Asistencia_Eventos.xlsx");
  };

  // Exportar a PDF
  const exportToPDF = () => {
    const doc = new jsPDF();
    doc.text("Reporte de Asistencia por Evento", 14, 15);
    doc.autoTable({
      head: [['Evento', 'Asistentes', 'Categoría', 'Lugar', 'Ciudad']],
      body: datos.map(item => [
        item.evento,
        item.asistentes,
        item.categoria,
        item.lugar,
        item.ciudad
      ]),
      startY: 20,
      styles: { fontSize: 8 },
      headStyles: { fillColor: [76, 175, 80] }
    });
    doc.save("Asistencia_Eventos.pdf");
  };

  // Cargar opciones de filtros
  useEffect(() => {
    const cargarOpciones = async () => {
      try {
        const [resCiudades, resCategorias] = await Promise.all([
          getCiudades(),
          getCategorias()
        ]);
        setCiudades(resCiudades.data);
        setCategorias(resCategorias.data);
      } catch (error) {
        console.error("Error cargando opciones:", error);
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
        const { data } = await getAsistenciaEvento(filtros);
        setDatos(data.data || []);
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
        <h2>Asistencia por Evento</h2>
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
            opciones: ciudades,
            opcionVacia: "Todas las ciudades"
          },
          {
            tipo: 'select',
            nombre: 'categoria_id',
            etiqueta: 'Categoría',
            opciones: categorias,
            opcionVacia: "Todas las categorías"
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
                label: `${item.evento} (${item.ciudad})`,
                value: item.asistentes
              }))}
              titulo="Asistentes por Evento"
            />
            
            <TablaResultados
              datos={datos}
              columnas={[
                { key: 'evento', titulo: 'Evento' },
                { key: 'asistentes', titulo: 'Asistentes' },
                { key: 'categoria', titulo: 'Categoría' },
                { key: 'ciudad', titulo: 'Ciudad' }
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