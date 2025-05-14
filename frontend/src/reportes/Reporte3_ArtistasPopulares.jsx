import { useState, useEffect } from 'react';
import { getArtistasPopulares, getTiposArtista } from '../api/reportesService';
import FiltrosReporte from '../components/FiltrosReporte';
import GraficaPastel from '../components/GraficaPastel';
import TablaResultados from '../components/TablaResultados';
import { utils as xlsxUtils, writeFile as xlsxWriteFile } from 'xlsx';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

export default function ReporteArtistasPopulares() {
  const [datos, setDatos] = useState([]);
  const [tiposArtista, setTiposArtista] = useState([]);
  const [loading, setLoading] = useState(false);

  const [filtros, setFiltros] = useState({
    fecha_inicio: '',
    fecha_fin: '',
    tipo_artista: '',
    min_eventos: 1,
    skip: 0,
    limit: 10
  });

  // Cargar opciones de filtros
  useEffect(() => {
    const cargarOpciones = async () => {
      try {
        const res = await getTiposArtista();
        setTiposArtista(res.data);
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
      try {
        const { data } = await getArtistasPopulares(filtros);
        setDatos(data.data || []);
      } catch (error) {
        console.error("Error cargando datos:", error);
      } finally {
        setLoading(false);
      }
    };
    cargarDatos();
  }, [filtros]);

  const exportToExcel = () => {
    const datosExportar = datos.map(item => ({
      'Artista': item.artista,
      'Tipo': item.tipo,
      'Eventos Participados': item.eventos_participados,
      'Total Asistentes': item.asistentes_totales
    }));

    const worksheet = xlsxUtils.json_to_sheet(datosExportar);
    const workbook = xlsxUtils.book_new();
    xlsxUtils.book_append_sheet(workbook, worksheet, "ArtistasPopulares");
    xlsxWriteFile(workbook, "Artistas_Populares.xlsx");
  };

  const exportToPDF = () => {
    const doc = new jsPDF();
    doc.text("Reporte de Artistas Populares", 14, 15);
    doc.autoTable({
      head: [['Artista', 'Tipo', 'Eventos', 'Asistentes']],
      body: datos.map(item => [
        item.artista,
        item.tipo,
        item.eventos_participados,
        item.asistentes_totales
      ]),
      startY: 20
    });
    doc.save("Artistas_Populares.pdf");
  };

  return (
    <div className="reporte-container">
      <div className="reporte-header">
        <h2>Artistas Populares</h2>
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
        onChange={setFiltros}
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
            nombre: 'tipo_artista',
            etiqueta: 'Tipo de Artista',
            opciones: tiposArtista,
            opcionVacia: "Todos los tipos"
          },
          {
            tipo: 'number',
            nombre: 'min_eventos',
            etiqueta: 'Mínimo de eventos',
            min: 1
          }
        ]}
      />

      {loading ? (
        <div>Cargando...</div>
      ) : datos.length === 0 ? (
        <div>No hay datos con los filtros seleccionados</div>
      ) : (
        <div className="visualizacion">
          <GraficaPastel
            datos={datos.map(item => ({
              label: item.artista,
              value: item.asistentes_totales
            }))}
            titulo="Distribución de Asistentes por Artista"
          />

          <TablaResultados
            datos={datos}
            columnas={[
              { key: 'artista', titulo: 'Artista' },
              { key: 'tipo', titulo: 'Tipo' },
              { key: 'eventos_participados', titulo: 'Eventos' },
              { key: 'asistentes_totales', titulo: 'Asistentes' }
            ]}
          />
        </div>
      )}
    </div>
  );
}