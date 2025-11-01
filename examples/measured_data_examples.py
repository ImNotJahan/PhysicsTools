from physics_utils import MeasuredData

def measured_data_examples():
    # Example 1: Basic Arithmetic with MeasuredData
    data1 = MeasuredData(10.0, 0.5, 0.2)
    data2 = MeasuredData(5.0, 0.3, 0.1)

    print("Data 1:", data1)
    print("Data 2:", data2)

    # Addition
    result_add = data1 + data2
    print("Addition Result:", result_add)

    # Subtraction
    result_sub = data1 - data2
    print("Subtraction Result:", result_sub)

    # Multiplication
    result_mul = data1 * data2
    print("Multiplication Result:", result_mul)

    # Division
    result_div = data1 / data2
    print("Division Result:", result_div)

    # Negation
    neg_data = -data1
    print("Negated Data 1:", neg_data)

    # Absolute Value
    abs_data = abs(data1)
    print("Absolute Data 1:", abs_data)

    # Example 2: Trigonometric Functions
    angle = MeasuredData(0.5, 0.01, 0.005)  # Angle in radians
    print("Angle:", angle)

    sine_result = angle.sine()
    print("Sine of Angle:", sine_result)

    cosine_result = angle.cosine()
    print("Cosine of Angle:", cosine_result)

    tangent_result = angle.tangent()
    print("Tangent of Angle:", tangent_result)

    # Example 3: String and LaTeX Representation
    data3 = MeasuredData(123.456, 0.789, 0.123)
    print("String Representation:", str(data3))
    print("LaTeX Representation:", data3.latex())

if __name__ == "__main__":
    measured_data_examples()
