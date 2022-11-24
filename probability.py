import math

import numpy as np


def calculate_brand_probability(brand, questions_so_far, answers_so_far, brands):
    # Prior
    p_brand = 1 / len(brands)

    # Likelihood
    p_answers_given_brand = 1
    p_answers_given_not_brand = 1
    for question, answer in zip(questions_so_far, answers_so_far):
        p_answers_given_brand *= max(
            1 - abs(answer - brand_answer(brand, question)), 0.01)

        p_answer_not_brand = np.mean([1 - abs(answer - brand_answer(not_brand, question))
                                        for not_brand in brands
                                        if not_brand['name'] != brand['name']])
        p_answers_given_not_brand *= max(p_answer_not_brand, 0.01)

    # Evidence
    p_answers = p_brand * p_answers_given_brand + (1 - p_brand) * p_answers_given_not_brand

    # Bayes Theorem
    p_brand_given_answers = (p_answers_given_brand * p_brand) / p_answers

    return p_brand_given_answers


def brand_answer(brand, question):
    if question in brand['answers']:
        return brand['answers'][question]
    return 0.5


def calculate_probabilities(questions_so_far, answers_so_far, brands):
    probabilities = []
    for brand in brands:
        probabilities.append({
            'name': brand['name'],
            'probability': calculate_brand_probability(brand, questions_so_far, answers_so_far, brands)
        })

    return probabilities
