import unittest
from physics_utils import MeasuredData
import math


class TestMeasuredData(unittest.TestCase):

    def test_error(self):
        data = MeasuredData(100.2, 2.4, 10.12)
        self.assertEqual(data.error(), 10.12)

    def test_int(self):
        data = MeasuredData(100.2, 2, 10)
        self.assertEqual(int(data), 100)

    def test_float(self):
        data = MeasuredData(100.2, 2, 10)
        self.assertEqual(float(data), 100.2)

    def test_add(self):
        data1 = MeasuredData(10.4, 0.0, 0.5)
        data2 = MeasuredData(3.0, 1.0, 0.2)
        result = data1 + data2
        self.assertAlmostEqual(result.value, 13.4)
        self.assertAlmostEqual(result.reading_error, math.sqrt(1.0))
        self.assertAlmostEqual(result.standard_error, math.sqrt(0.5**2 + 0.2**2))

    def test_sub(self):
        data1 = MeasuredData(10.4, 0.0, 0.5)
        data2 = MeasuredData(3.0, 1.0, 0.2)
        result = data1 - data2
        self.assertAlmostEqual(result.value, 7.4)
        self.assertAlmostEqual(result.reading_error, math.sqrt(1.0))
        self.assertAlmostEqual(result.standard_error, math.sqrt(0.5**2 + 0.2**2))

    def test_mul(self):
        data1 = MeasuredData(10.0, 0.5, 0.2)
        data2 = MeasuredData(2.0, 0.1, 0.05)
        result = data1 * data2
        self.assertAlmostEqual(result.value, 20.0)
        self.assertAlmostEqual(result.reading_error, 20.0 * math.sqrt((0.5/10.0)**2 + (0.1/2.0)**2))
        self.assertAlmostEqual(result.standard_error, 20.0 * math.sqrt((0.2/10.0)**2 + (0.05/2.0)**2))

    def test_truediv(self):
        data1 = MeasuredData(10.0, 0.5, 0.2)
        data2 = MeasuredData(2.0, 0.1, 0.05)
        result = data1 / data2
        self.assertAlmostEqual(result.value, 5.0)
        self.assertAlmostEqual(result.reading_error, 5.0 * math.sqrt((0.5/10.0)**2 + (0.1/2.0)**2))
        self.assertAlmostEqual(result.standard_error, 5.0 * math.sqrt((0.2/10.0)**2 + (0.05/2.0)**2))

    def test_pow(self):
        data = MeasuredData(2.0, 0.1, 0.05)
        result = data ** 3
        self.assertAlmostEqual(result.value, 8.0)
        self.assertAlmostEqual(result.reading_error, abs(3 * 2.0**2 * 0.1))
        self.assertAlmostEqual(result.standard_error, abs(3 * 2.0**2 * 0.05))

    def test_sine(self):
        data = MeasuredData(math.pi / 2, 0.1, 0.05)
        result = data.sine()
        self.assertAlmostEqual(result.value, 1.0)
        self.assertAlmostEqual(result.reading_error, abs(0.1 * math.cos(math.pi / 2)))
        self.assertAlmostEqual(result.standard_error, abs(0.05 * math.cos(math.pi / 2)))

    def test_cosine(self):
        data = MeasuredData(0, 0.1, 0.05)
        result = data.cosine()
        self.assertAlmostEqual(result.value, 1.0)
        self.assertAlmostEqual(result.reading_error, abs(0.1 * math.sin(0)))
        self.assertAlmostEqual(result.standard_error, abs(0.05 * math.sin(0)))

    def test_tangent(self):
        data = MeasuredData(math.pi / 4, 0.1, 0.05)
        result = data.tangent()
        self.assertAlmostEqual(result.value, 1.0)

    def test_arctan(self):
        data = MeasuredData(1.0, 0.1, 0.05)
        result = data.arctan()
        self.assertAlmostEqual(result.value, math.atan(1.0))
        self.assertAlmostEqual(result.reading_error, 0.1 / (1 + 1.0**2))
        self.assertAlmostEqual(result.standard_error, 0.05 / (1 + 1.0**2))

    def test_arcsin(self):
        data = MeasuredData(0.5, 0.1, 0.05)
        result = data.arcsin()
        self.assertAlmostEqual(result.value, math.asin(0.5))
        self.assertAlmostEqual(result.reading_error, 0.1 / math.sqrt(1 - 0.5**2))
        self.assertAlmostEqual(result.standard_error, 0.05 / math.sqrt(1 - 0.5**2))

    def test_neg(self):
        data = MeasuredData(10.0, 0.5, 0.2)
        result = -data
        self.assertEqual(result.value, -10.0)
        self.assertEqual(result.error(), 0.5)

    def test_abs(self):
        data = MeasuredData(-10.0, 0.5, 0.2)
        result = abs(data)
        self.assertEqual(result.value, 10.0)
        self.assertEqual(result.reading_error, 0.5)
        self.assertEqual(result.standard_error, 0.2)

    def test_str(self):
        data = MeasuredData(1234.56789, 0.05333)
        self.assertEqual(str(data), '1234.57±0.05')

    def test_latex(self):
        data = MeasuredData(1234.56789, 0.05333)
        self.assertEqual(data.latex(), '$1234.57 \\pm 0.05$')


if __name__ == '__main__':
    unittest.main()


class TestEdgeCases(unittest.TestCase):

    def test_atan_float(self):
        from physics_utils.data import math as pm
        self.assertAlmostEqual(pm.atan(1.0), math.pi / 4)

    def test_pow_uncertain_exponent(self):
        result = MeasuredData(2, 0) ** MeasuredData(3, 0.1)
        self.assertAlmostEqual(result.reading_error, 8 * math.log(2) * 0.1)

    def test_pow_both_uncertain(self):
        result = MeasuredData(2, 0.1) ** MeasuredData(3, 0.1)
        expected = math.sqrt((3 * 2 ** 2 * 0.1) ** 2 + (8 * math.log(2) * 0.1) ** 2)
        self.assertAlmostEqual(result.reading_error, expected)

    def test_mul_zero_value_keeps_error(self):
        self.assertAlmostEqual((MeasuredData(0, 0.1) * 5).reading_error, 0.5)
        self.assertAlmostEqual((MeasuredData(0, 0.1) * MeasuredData(3, 0.1)).reading_error, 0.3)

    def test_div_zero_numerator(self):
        result = MeasuredData(0, 0.1) / MeasuredData(3, 0.1)
        self.assertEqual(result.value, 0)
        self.assertAlmostEqual(result.reading_error, 0.1 / 3)

    def test_div_by_zero_still_raises(self):
        with self.assertRaises(ZeroDivisionError):
            MeasuredData(2, 0.1) / MeasuredData(0, 0.1)

    def test_negative_scalar_error_is_positive(self):
        self.assertAlmostEqual((MeasuredData(4, 0.5) * -2).reading_error, 1.0)
        self.assertAlmostEqual((MeasuredData(4, 0.5) / -2).reading_error, 0.25)
        self.assertAlmostEqual((2 / MeasuredData(-4, 0.5)).reading_error, 2 * 0.5 / 16)

    def test_mul_matches_relative_form(self):
        a, b = MeasuredData(10.0, 0.5), MeasuredData(2.0, 0.1)
        expected = 20 * math.sqrt((0.5 / 10) ** 2 + (0.1 / 2) ** 2)
        self.assertAlmostEqual((a * b).reading_error, expected)
        self.assertAlmostEqual((a / b).reading_error, 5 * math.sqrt((0.5 / 10) ** 2 + (0.1 / 2) ** 2))

    def test_hashable(self):
        self.assertEqual(len({MeasuredData(1, 0.1), MeasuredData(1, 0.2)}), 1)


class TestAveraging(unittest.TestCase):

    def test_avg_from_set_standard_error(self):
        from physics_utils.data import avg_from_set
        result = avg_from_set([1.0, 2.0, 3.0, 4.0], 0.1)
        self.assertAlmostEqual(result.value, 2.5)
        self.assertAlmostEqual(result.standard_error, 1.2909944487358056 / 2)
        self.assertEqual(result.reading_error, 0.1)

    def test_avg_measured_datas(self):
        from physics_utils.data import avg_measured_datas
        data = [MeasuredData(v, 0.3) for v in (1.0, 2.0, 3.0, 4.0)]
        result = avg_measured_datas(data)
        self.assertAlmostEqual(result.reading_error, 0.3 / 2)
        self.assertAlmostEqual(result.standard_error, 1.2909944487358056 / 2)

    def test_single_measurement(self):
        from physics_utils.data import avg_from_set
        self.assertEqual(avg_from_set([5.0], 0.1).standard_error, 0.0)


if __name__ == "__main__":
    unittest.main()
