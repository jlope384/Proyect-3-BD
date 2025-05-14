import { useState, useEffect } from 'react';
import { getEventosPorCategoria, getCategorias } from '../api/reportesService';
import FiltrosReporte from '../components/FiltrosReporte';
import GraficaBarras from '../components/GraficaBarras';
import TablaResultados from '../components/TablaResultados';
import { utils as xlsxUtils, writeFile as xlsxWriteFile } from 'xlsx';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

export default function ReporteEventosPorCategoria() {
  const [datos, setDatos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [filtros, setFiltros] = useState({
    fecha_inicio: '',
    fecha_fin: '',
    categoria_id: '', // Nuevo filtro añadido
    ingresos_minimos: 0,
    skip: 0,
    limit: 10
  });

  // Cargar opciones de filtros
  useEffect(() => {
    const cargarOpciones = async () => {
      try {
        const res = await getCategorias();
        setCategorias(res.data);
      } catch (error) {
        console.error("Error cargando categorías:", error);
        setError("Error al cargar categorías");
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
        const { data } = await getEventosPorCategoria(filtros);
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

  const exportToExcel = () => {
    const datosExportar = datos.map(item => ({
      'Categoría': item.categoria,
      'Total Eventos': item.total_eventos,
      'Ingresos Totales': item.ingresos_totales,
      'Promedio Ingresos': item.promedio_ingresos
    }));

    const worksheet = xlsxUtils.json_to_sheet(datosExportar);
    const workbook = xlsxUtils.book_new();
    xlsxUtils.book_append_sheet(workbook, worksheet, "EventosPorCategoria");
    xlsxWriteFile(workbook, "Eventos_Por_Categoria.xlsx");
  };

  const exportToPDF = () => {
    const doc = new jsPDF();
    doc.text("Reporte de Eventos por Categoría", 14, 15);
    doc.autoTable({
      head: [['Categoría', 'Eventos', 'Ingresos (GTQ)', 'Promedio (GTQ)']],
      body: datos.map(item => [
        item.categoria,
        item.total_eventos,
        `Q${item.ingresos_totales.toFixed(2)}`,
        `Q${item.promedio_ingresos.toFixed(2)}`
      ]),
      startY: 20,
      styles: { fontSize: 8 },
      headStyles: { fillColor: [76, 175, 80] }
    });
    doc.save("Eventos_Por_Categoria.pdf");
  };

  return (
    <div className="reporte-container">
      <div className="reporte-header">
        <h2>Eventos por Categoría</h2>
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
            nombre: 'categoria_id',
            etiqueta: 'Categoría',
            opciones: categorias,
            opcionVacia: "Todas las categorías"
          },
          {
            tipo: 'number',
            nombre: 'ingresos_minimos',
            etiqueta: 'Ingresos Mínimos (GTQ)',
            min: 0,
            step: 100
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
        <div className="visualizacion">
          <GraficaBarras
            datos={datos.map(item => ({
              label: item.categoria,
              value: item.total_eventos
            }))}
            titulo="Eventos por Categoría"
          />

          <TablaResultados
            datos={datos}
            columnas={[
              { key: 'categoria', titulo: 'Categoría' },
              { key: 'total_eventos', titulo: 'Total Eventos' },
              { 
                key: 'ingresos_totales', 
                titulo: 'Ingresos Totales', 
                formato: (val) => `Q${val.toFixed(2)}` 
              },
              { 
                key: 'promedio_ingresos', 
                titulo: 'Promedio', 
                formato: (val) => `Q${val.toFixed(2)}` 
              }
            ]}
          />
        </div>
      )}
    </div>
  );
}