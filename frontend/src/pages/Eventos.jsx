import { useEffect, useState } from 'react';
import { getEventos } from '../api/eventosService';
import TablaResultados from '../components/TablaResultados';

const Eventos = () => {
  const [eventos, setEventos] = useState([]);

  const cargarEventos = async (filtros = {}) => {
    const data = await getEventos(filtros);
    setEventos(data);
  };

  useEffect(() => {
    cargarEventos();
  }, []);

  return (
    <div className="contenedor-pagina">
      <h1>Listado de Eventos</h1>
      <TablaResultados
        datos={eventos}
        columnas={['id', 'nombre', 'fecha', 'hora', 'lugar']}
        onFiltrar={cargarEventos}
      />
    </div>
  );
};

export default Eventos;