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
