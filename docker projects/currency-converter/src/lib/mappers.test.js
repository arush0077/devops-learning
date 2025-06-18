import { describe, it, expect } from 'vitest';
import { mapCurrencyData } from './mappers';

describe('mapCurrencyData', () => {
  it('should map currency data correctly', () => {
    const apiResponse = {
      response: {
        '2024-08-01': { USD: '1.1234' },
        '2024-08-02': { USD: '1.2345' },
      },
    };

    const expected = [
      { date: '2024-08-01', value: '1.12' },
      { date: '2024-08-02', value: '1.23' },
    ];

    expect(mapCurrencyData(apiResponse)).toEqual(expected);
  });
});
