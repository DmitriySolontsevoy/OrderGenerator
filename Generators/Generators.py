import math


class Generators:
    # Absolute value of cosine
    @staticmethod
    def absolute_cosine_generate(seed):
        return abs(math.cos(seed))

    @staticmethod
    # Absolute value of sine
    def absolute_sine_generate(seed):
        return abs(math.sin(seed))

    @staticmethod
    # Exponential function of a sine value
    def exponent_sine_generate(seed):
        return math.exp(math.sin(seed))

    @staticmethod
    # Absolute value of sine of cosine
    def absolute_sine_cosine_generate(seed):
        return abs(math.sin(math.cos(seed)))

    @staticmethod
    # Linear congruent method generation
    def linear_congruent_generate(prev_value, multiplier, offset, divisor):
        return (multiplier * prev_value + offset) % divisor
