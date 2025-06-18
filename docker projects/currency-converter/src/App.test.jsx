import { describe, it, expect, vi, beforeAll } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import App from './App';

vi.mock('./hooks/useFetchCurrency/useFetchCurrency', () => ({
  default: vi.fn(() => ({
    data: [
      { date: '2024-09-09', value: '1.25' },
      { date: '2024-09-10', value: '1.20' },
    ],
    loading: false,
    error: null,
  })),
}));

beforeAll(() => {
  global.ResizeObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
  };
});

describe('App Component', () => {
  it('renders without crashing', () => {
    const { container } = render(<App />);
    expect(container).toBeDefined();
  });

  it('displays currency conversion results correctly when data is loaded', async () => {
    vi.mock('./hooks/useFetchCurrency/useFetchCurrency', () => ({
      default: vi.fn(() => ({
        data: [
          { date: '2024-09-10', value: '4.67' },
          { date: '2024-09-11', value: '4.25' },
        ],
        loading: false,
        error: null,
      })),
    }));

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/1 USD/i)).toBeInTheDocument();
      expect(screen.getByText(/4.25 BRL/i)).toBeInTheDocument();
    });
  });
});
