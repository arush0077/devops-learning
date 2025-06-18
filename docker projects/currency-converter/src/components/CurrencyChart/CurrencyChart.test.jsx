import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { render } from '@testing-library/react';
import CurrencyChart from './CurrencyChart';

beforeAll(() => {
  global.ResizeObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
  };
});

afterAll(() => {
  delete global.ResizeObserver;
});

describe('<CurrencyChart />', () => {
  const mockData = [
    { date: '2024-08-01', value: 1.2 },
    { date: '2024-08-02', value: 1.3 },
    { date: '2024-08-03', value: 1.4 },
    { date: '2024-08-04', value: 1.5 },
    { date: '2024-08-05', value: 1.6 },
  ];

  it('renders the chart component', () => {
    const { container } = render(<CurrencyChart data={mockData} period="5" />);

    expect(container).not.toBeEmptyDOMElement();
  });
});
