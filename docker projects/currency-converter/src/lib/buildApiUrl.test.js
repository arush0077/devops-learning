import { describe, it, expect } from 'vitest';
import { buildApiUrl } from './buildApiUrl';
import { API_URL } from '../../constants';

describe('buildApiUrl', () => {
  it('should generate the correct URL', () => {
    const baseCurrency = 'USD';
    const targetCurrency = 'EUR';
    const period = 30;
    const endDate = new Date().toISOString().split('T')[0];
    const startDate = new Date(
      new Date().setDate(new Date().getDate() - period)
    )
      .toISOString()
      .split('T')[0];

    const expectedUrl = `${API_URL}&base=${baseCurrency}&start_date=${startDate}&end_date=${endDate}&symbols=${targetCurrency}`;
    expect(buildApiUrl(baseCurrency, targetCurrency, period)).toBe(expectedUrl);
  });
});
