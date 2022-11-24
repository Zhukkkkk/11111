from Tree import *
from utils import *
from probability import *


def main():
    categories = create_categories()
    brands_answers, brands = load_data()

    questions_dict = {}
    brands_questions = list(range(27))
    question_numbers = list(range(27))
    for i in question_numbers:
        questions_dict[i] = brands_questions[i]

    t = Tree()
    questions_number = len(brands[0]) - 1

    questions_so_far = []
    answers_so_far = []
    deleted_questions = 0

    while True:

        my_tree = t.build_tree(brands)
        if isinstance(my_tree, Leaf):
            confirm_answer(result, answers_so_far, questions_so_far, questions_number, brands_answers, True,
                           brands)
            break

        question = my_tree.question
        key = str(question.column)
        answer_value = -1

        print(question)
        while answer_value < 0:
            answer = input()
            answer_value = match_answer(answer)

        brands_answers_question = find_value(questions_dict, int(key))
        questions_so_far.append(str(brands_answers_question))
        answers_so_far.append(float(answer_value))

        brands_probabilities = calculate_probabilities(questions_so_far, answers_so_far, brands_answers)
        result = sorted(brands_probabilities, key=lambda p: p['probability'], reverse=True)
        print("probabilities", result)

        if answer == 'да':
            category = find_category(categories, int(key))
            brands_questions = update_questions(brands_questions, categories[category])
            deleted_questions += delete_category(brands, category, categories, t.headers)
            update_questions_in_categories(categories)
            if len(questions_so_far) > 2:
                delete_brands(brands_probabilities, brands_answers)

        elif answer == 'нет' or answer == 'не знаю' or answer == 'скорее нет' or answer == 'возможно частично':
            brands_questions = update_questions(brands_questions, [int(key)])
            delete_question(brands, int(key), categories)
            delete_header(t.headers, int(key))
            update_questions_in_categories(categories)
            if len(questions_so_far) > 2:
                delete_brands(brands_probabilities, brands_answers)

        for i in question_numbers:
            questions_dict[i] = brands_questions[i]

        if check_prob(result) or len(questions_so_far) == 15:
            if confirm_answer(result, answers_so_far, questions_so_far, questions_number, brands_answers,
                              False, brands):
                break

        brands_probabilities = calculate_probabilities(questions_so_far, answers_so_far, brands_answers)
        result = sorted(brands_probabilities, key=lambda p: p['probability'], reverse=True)


if __name__ == "__main__":
    while True:
        main()
        print('Хотите начать новую игру?')

        while True:
            new_game = input()
            if new_game == "да" or new_game == "нет":
                break
        if new_game == 'нет':
            break
