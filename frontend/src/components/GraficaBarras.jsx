import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chart.js/auto';

const GraficaBarras = ({ datos, titulo }) => {
  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: titulo }
    }
  };

  const data = {
    labels: datos.map(item => item.label),
    datasets: [{
      label: 'Total',
      data: datos.map(item => item.value),
      backgroundColor: '#4CAF50'
    }]
  };

  return <Bar options={options} data={data} />;
};

export default GraficaBarras;