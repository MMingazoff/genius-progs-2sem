class NewInt:
    def __init__(self, number):
        self.digits = dict()
        self._fill_dict(number)

    def __add__(self, other):
        if len(self.digits) < len(other.digits):
            return other + self
        new_num = self.copy()
        for tenth_pow in range(min(len(self.digits), len(other.digits)) - 1):
            new_num.digits[tenth_pow] = self.digits[tenth_pow] + other.digits[tenth_pow]
            if new_num.digits[tenth_pow] >= 10:
                new_num.digits[tenth_pow + 1] = self.digits.get(tenth_pow + 1, 0) + 1
                new_num.digits[tenth_pow] -= 10
        return new_num

    def copy(self):
        new_num = NewInt(0)
        for k, v in self.digits.items():
            new_num.digits[k] = v
        return new_num

    def __sub__(self, other):
        if self.digits["sign"] == 1 and other.digits["sign"] == 1:
            sub1 = other.copy()
            sub2 = self.copy()
            sub1.digits["sign"] = 0
            return -(sub1 - sub2)
        elif self.digits["sign"] == 0 and other.digits["sign"] == 1:
            sub2 = other.copy()
            sub2.digits["sign"] = 0
            return self + sub2
        elif self.digits["sign"] == 1 and other.digits["sign"] == 0:
            sub1 = self.copy()
            sub2 = other.copy()
            sub1.digits["sign"] = 0
            return -(sub1 + sub2)
        if self < other:
            sub1 = other.copy()
            sub2 = self.copy()
            sub1.digits["sign"] = 1
        else:
            sub1 = self.copy()
            sub2 = other.copy()
        for tenth_pow in range(min(len(sub1.digits), len(sub2.digits)) - 1):
            sub1.digits[tenth_pow] -= sub2.digits[tenth_pow]
            if sub1.digits[tenth_pow] < 0:
                sub1.digits[tenth_pow + 1] -= 1
                sub1.digits[tenth_pow] += 10
        return sub1

    def __neg__(self):
        new_num = self.copy()
        sign = new_num.digits["sign"]
        new_num.digits["sign"] = 0 if sign != 0 else 1
        return new_num

    def __eq__(self, other):
        if len(self.digits) != len(other.digits) or self.digits["sign"] != other.digits["sign"]:
            return False
        for tenth_pow in range(len(self.digits) - 1):
            if self.digits[tenth_pow] != other.digits[tenth_pow]:
                return False
        return True

    def __lt__(self, other):
        if self.digits["sign"] < other.digits["sign"] or len(self.digits) > len(other.digits):
            return False
        elif self.digits["sign"] > other.digits["sign"] or len(self.digits) < len(other.digits):
            return True
        for tenth_pow in range(len(self.digits) - 2, -1, -1):
            if self.digits[tenth_pow] == other.digits[tenth_pow]:
                continue
            if self.digits[tenth_pow] < other.digits[tenth_pow]:
                return True
            return False
        return False

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not(self < other)

    def __ge__(self, other):
        return self == other or self > other

    def __ne__(self, other):
        return not(self == other)

    def _fill_dict(self, number):
        tmp = abs(number)
        self.digits["sign"] = 0 if number >= 0 else 1
        tenth_pow = 0
        while tmp > 0:
            self.digits[tenth_pow] = tmp % 10
            tmp //= 10
            tenth_pow += 1

    def __str__(self):
        digits_powers = list(filter(lambda el: isinstance(el[0], int), self.digits.items()))
        digits_powers = sorted(digits_powers, key=lambda tpl: tpl[0], reverse=True)
        return ''.join(['' if self.digits["sign"] == 0 else '-'] + [str(tpl[1]) for tpl in digits_powers])

    __repr__ = __str__


if __name__ == '__main__':
    a = NewInt(123)
    b = NewInt(23)
    c = NewInt(123)
    print(a, b)
    print(a+b)
    print(a, b)
    print(-a)
    print(a)
    print(a < b)
    print(a, b)
    print(b - a)
    print(a == c)
