import PropTypes from 'prop-types';
import Flag from 'react-world-flags';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

const CurrencyInput = ({
  currencyOptions,
  amount,
  currency,
  onAmountChange,
  onCurrencyChange,
}) => {
  return (
    <div className="flex w-full lg:w-[500px] lg:flex-row items-center border border-custom-grey p-3 rounded-xl bg-custom-grey">
      <Select
        onValueChange={onCurrencyChange}
        value={currency}
        className="flex items-center mb-2 sm:mb-0"
      >
        <SelectTrigger className="w-full sm:w-[220px] border-none bg-custom-grey text-white">
          <SelectValue placeholder="" className="text-white" />
        </SelectTrigger>
        <SelectContent className="border-none bg-custom-grey">
          {currencyOptions.map(({ currency, name, flag }) => (
            <SelectItem
              key={currency}
              value={currency}
              className="flex items-center py-2 px-8 hover:bg-gray-200 cursor-pointer"
            >
              <div className="flex items-center">
                <div className="w-6 h-6 mr-2">
                  <Flag className="w-6 h-6 mr-2" code={flag} />
                </div>
                <span className="text-white">{name}</span>
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      <Input
        type="text"
        value={amount}
        onChange={(e) => onAmountChange(e.target.value)}
        className="w-full sm:w-[150px] ml-0 sm:ml-2 border-none rounded-none bg-custom-grey text-white-800"
      />
    </div>
  );
};

CurrencyInput.propTypes = {
  currencyOptions: PropTypes.arrayOf(
    PropTypes.shape({
      flag: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
      currency: PropTypes.string.isRequired,
    })
  ).isRequired,
  amount: PropTypes.string,
  currency: PropTypes.string,
  onAmountChange: PropTypes.func,
  onCurrencyChange: PropTypes.func,
};

export default CurrencyInput;
