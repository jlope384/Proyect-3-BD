import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chart.js/auto';

const GraficaPastel = ({ datos, titulo }) => {
  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'right' },
      title: { display: true, text: titulo }
    }
  };

  const data = {
    labels: datos.map(item => item.label),
    datasets: [{
      data: datos.map(item => item.value),
      backgroundColor: [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
        '#9966FF', '#FF9F40', '#8AC24A', '#607D8B'
      ]
    }]
  };

  return <Pie options={options} data={data} />;
};

export default GraficaPastel;