import PropTypes from 'prop-types';
import { CartesianGrid, Line, LineChart, XAxis, YAxis } from 'recharts';
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart';

const chartConfig = {
  value: {
    label: 'Valor',
    color: '#747bff',
  },
};

function CurrencyChart({ data, period }) {
  const sortedData = Array.isArray(data)
    ? [...data].sort((a, b) => new Date(a.date) - new Date(b.date))
    : [];

  const filteredData = period === '30' ? sortedData : sortedData.slice(-5);

  const values = filteredData.map((d) => d.value);
  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);
  const padding = (maxValue - minValue) * 0.2;

  return (
    <ChartContainer config={chartConfig} className={'h-[350px] w-full'}>
      <LineChart
        accessibilityLayer
        data={filteredData}
        margin={{
          left: 4,
          right: 4,
          bottom: 60,
        }}
      >
        <CartesianGrid
          strokeDasharray="3 3"
          stroke="#e0e0e0"
          horizontal={true}
          vertical={false}
        />
        <YAxis
          type="number"
          domain={[minValue - padding, maxValue + padding]}
        />
        <XAxis
          dataKey="date"
          tickLine={true}
          axisLine={true}
          tickMargin={8}
          angle={-45}
          textAnchor="end"
        />
        <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
        <Line dataKey="value" type="natural" stroke="#747bff" strokeWidth={1} />
      </LineChart>
    </ChartContainer>
  );
}

CurrencyChart.propTypes = {
  data: PropTypes.arrayOf(
    PropTypes.shape({
      date: PropTypes.string.isRequired,
      value: PropTypes.string.isRequired,
    })
  ).isRequired,
  period: PropTypes.oneOf(['5', '30']).isRequired,
};

export default CurrencyChart;
