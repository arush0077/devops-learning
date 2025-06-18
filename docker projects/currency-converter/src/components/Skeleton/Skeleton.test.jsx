import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import Skeleton from './Skeleton';

describe('<Skeleton />', () => {
  it('renders the Skeleton component', () => {
    const { container } = render(<Skeleton />);

    const skeletonElements = container.querySelectorAll('.skeleton');
    expect(skeletonElements).toHaveLength(3);
  });
});
