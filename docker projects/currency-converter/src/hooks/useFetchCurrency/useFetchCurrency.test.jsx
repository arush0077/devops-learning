import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import useFetchCurrency from './useFetchCurrency';
import { buildApiUrl } from '@/lib/buildApiUrl';
import { mapCurrencyData } from '@/lib/mappers';

vi.mock('@/lib/buildApiUrl');
vi.mock('@/lib/mappers');

describe('useFetchCurrency', () => {
  const baseCurrency = 'USD';
  const targetCurrency = 'EUR';
  const cachedData = [{ date: '2024-08-14', rate: 1.2 }];

  beforeEach(() => {
    buildApiUrl.mockReturnValue('mocked-url');
    mapCurrencyData.mockReturnValue(cachedData);
    global.fetch = vi.fn();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('should fetch currency data and update state', async () => {
    const mockData = { rates: [{ date: '2024-08-14', rate: 1.2 }] };
    fetch.mockResolvedValueOnce({
      ok: true,
      json: vi.fn().mockResolvedValueOnce(mockData),
    });

    const { result } = renderHook(() =>
      useFetchCurrency(baseCurrency, targetCurrency)
    );

    expect(result.current.loading).toBe(true);
    expect(result.current.data).toBeNull();

    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 500));
    });

    expect(buildApiUrl).toHaveBeenCalledWith(baseCurrency, targetCurrency, 30);
    expect(fetch).toHaveBeenCalledWith('mocked-url');
    expect(mapCurrencyData).toHaveBeenCalledWith(mockData);
    expect(result.current.data).toEqual(cachedData);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it('should handle fetch error and update error state', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
    });

    const { result } = renderHook(() =>
      useFetchCurrency(baseCurrency, targetCurrency)
    );

    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 500));
    });

    expect(result.current.loading).toBe(false);
    expect(result.current.data).toBeNull();
    expect(result.current.error).toBe('Erro ao buscar os dados');
  });
});
