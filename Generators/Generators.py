from Services.Logger.Implementation.TextFileLogger import TextFileLogger
import math


class Generators:
    # Absolute value of cosine
    @staticmethod
    def absolute_cosine_generate(number):
        num = abs(math.cos(number))
        TextFileLogger.debug("absolute_cosine_generate(): Generated abs(cos): " + str(num))
        return num

    @staticmethod
    # Absolute value of sine
    def absolute_sine_generate(number):
        num = abs(math.sin(number))
        TextFileLogger.debug("absolute_sine_generate(): Generated abs(sin): " + str(num))
        return num

    @staticmethod
    # Exponential function of a sine value
    def exponent_sine_generate(number):
        num = math.exp(math.sin(number))
        TextFileLogger.debug("exponent_sine_generate(): Generated exp(sin): " + str(num))
        return num

    @staticmethod
    # Absolute value of sine of cosine
    def absolute_sine_cosine_generate(number):
        num = abs(math.sin(math.cos(number)))
        TextFileLogger.debug("absolute_sine_cosine_generate(): Generated sin(cos): " + str(num))
        return num

    @staticmethod
    # Linear congruent method generation
    def linear_congruent_generate(prev_value, multiplier, offset, divisor):
        num = (multiplier * prev_value + offset) % divisor
        TextFileLogger.debug("linear_congruent_generate(): Generated (a*Xn-1 + c) % m: " + str(num))
        return num
