import { useState, useEffect } from 'react';
import { getAsistenciaEvento } from '../api/reportesService';
import FiltrosReporte from '../components/FiltrosReporte';
import GraficaBarras from '../components/GraficaBarras';
import TablaResultados from '../components/TablaResultados';

export default function ReporteAsistenciaEvento() {
  const [datos, setDatos] = useState([]);
  const [filtros, setFiltros] = useState({
    fecha_inicio: '',
    fecha_fin: '',
    ciudad_id: null,
    categoria_id: null
  });

  const cargarDatos = async () => {
    try {
      const { data } = await getAsistenciaEvento(filtros);
      setDatos(data);
    } catch (error) {
      console.error('Error cargando datos:', error);
    }
  };

  useEffect(() => { cargarDatos(); }, [filtros]);

  return (
    <div className="reporte-container">
      <h2>Asistencia por Evento</h2>
      
      <FiltrosReporte 
        filtros={filtros}
        onChange={setFiltros}
        campos={[
          { tipo: 'fecha', nombre: 'fecha_inicio', etiqueta: 'Fecha Inicio' },
          { tipo: 'fecha', nombre: 'fecha_fin', etiqueta: 'Fecha Fin' },
          { 
            tipo: 'select', 
            nombre: 'categoria_id', 
            etiqueta: 'Categoría',
            opciones: [
              { id: 1, nombre: 'Música' },
              { id: 2, nombre: 'Arte' }
            ]
          }
        ]}
      />

      <div className="visualizacion">
        <GraficaBarras 
          datos={datos.map(item => ({
            label: item.evento,
            value: item.asistentes
          }))} 
          titulo="Asistencia por Evento"
        />
        
        <TablaResultados 
          datos={datos}
          columnas={['evento', 'asistentes', 'categoria']}
        />
      </div>
    </div>
  );
}