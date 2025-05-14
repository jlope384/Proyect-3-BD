import { useState, useEffect } from 'react';
import { getVentasTotales, getTiposEntrada, getMediosPago } from '../api/reportesService';
import FiltrosReporte from '../components/FiltrosReporte';
import GraficaBarras from '../components/GraficaBarras';
import TablaResultados from '../components/TablaResultados';
import { utils as xlsxUtils, writeFile as xlsxWriteFile } from 'xlsx';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

export default function ReporteVentasTotales() {
  const [datos, setDatos] = useState([]);
  const [tiposEntrada, setTiposEntrada] = useState([]);
  const [mediosPago, setMediosPago] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [filtros, setFiltros] = useState({
    fecha_inicio: '',
    fecha_fin: '',
    tipo_entrada_id: '',
    medio_pago_id: '',
    skip: 0,
    limit: 10
  });

  // Exportar a Excel
  const exportToExcel = () => {
    const datosExportar = datos.map(item => ({
      'Evento': item.evento,
      'Tipo Entrada': item.tipo_entrada,
      'Medio Pago': item.medio_pago,
      'Cantidad': item.cantidad,
      'Total (GTQ)': item.total
    }));

    const worksheet = xlsxUtils.json_to_sheet(datosExportar);
    const workbook = xlsxUtils.book_new();
    xlsxUtils.book_append_sheet(workbook, worksheet, "VentasTotales");
    xlsxWriteFile(workbook, "Ventas_Totales.xlsx");
  };

  // Exportar a PDF
  const exportToPDF = () => {
    const doc = new jsPDF();
    doc.text("Reporte de Ventas Totales", 14, 15);
    doc.autoTable({
      head: [['Evento', 'Tipo Entrada', 'Medio Pago', 'Cantidad', 'Total (GTQ)']],
      body: datos.map(item => [
        item.evento,
        item.tipo_entrada,
        item.medio_pago,
        item.cantidad,
        `Q${item.total.toFixed(2)}`
      ]),
      startY: 20,
      styles: { fontSize: 8 },
      headStyles: { fillColor: [76, 175, 80] }
    });
    doc.save("Ventas_Totales.pdf");
  };

  // Cargar opciones de filtros
  useEffect(() => {
    const cargarOpciones = async () => {
      try {
        const [resTipos, resMedios] = await Promise.all([
          getTiposEntrada(),
          getMediosPago()
        ]);
        setTiposEntrada(resTipos.data);
        setMediosPago(resMedios.data);
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
        const { data } = await getVentasTotales(filtros);
        setDatos(data.data || []);
      } catch (error) {
        console.error("Error cargando datos:", error);
        setError("Error al cargar ventas. Verifica la conexión.");
      } finally {
        setLoading(false);
      }
    };
    cargarDatos();
  }, [filtros]);

  return (
    <div className="reporte-container">
      <div className="reporte-header">
        <h2>Ventas Totales</h2>
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
            nombre: 'tipo_entrada_id', 
            etiqueta: 'Tipo de Entrada',
            opciones: tiposEntrada,
            opcionVacia: "Todos los tipos"
          },
          { 
            tipo: 'select', 
            nombre: 'medio_pago_id', 
            etiqueta: 'Medio de Pago',
            opciones: mediosPago,
            opcionVacia: "Todos los medios"
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
                label: `${item.evento} (${item.tipo_entrada})`,
                value: item.total
              }))}
              titulo="Ventas por Evento (GTQ)"
            />
            
            <TablaResultados 
              datos={datos}
              columnas={[
                { key: 'evento', titulo: 'Evento' },
                { key: 'tipo_entrada', titulo: 'Tipo Entrada' },
                { key: 'medio_pago', titulo: 'Medio Pago' },
                { key: 'cantidad', titulo: 'Entradas Vendidas' },
                { key: 'total', titulo: 'Total (GTQ)', formato: (val) => `Q${val.toFixed(2)}` }
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
