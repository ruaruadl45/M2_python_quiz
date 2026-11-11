# Quiz Game
def get_valid_number(prompt, min_value, max_value):
    while True:
        value = input(prompt).strip()

        try:
            value = int(value)

            if min_value <= value <= max_value:
                return value
            else:
                print(f"{min_value}~{max_value} 사이의 숫자를 입력하세요.")

        except ValueError:
            print("숫자만 입력할 수 있습니다.")

# Quiz class
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print(self.question)

        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    def check_answer(self, user_answer):
        return self.answer == user_answer

# Quiz data
quizzes = [
    Quiz(
        "조선시대부터 불리던 대전의 옛 이름으로, '큰밭'이라는 순우리말에서 유래한 지명은 무엇인가요?",
        ["누리밭", "한밭", "솔밭", "늘밭"],
        2
    ),
    Quiz(
        "대한민국 과학기술의 중심지 역할을 하는 대전의 대규모 연구개발 단지의 이름은 무엇인가요?",
        ["대덕연구개발특구", "송도국제연구단지", "오송생명과학단지", "판교테크노밸리"],
        1
    ),
    Quiz(
        "1993년에 개최된 대전 엑스포의 공식 마스코트 이름은 무엇인가요?",
        ["반다비", "수호랑", "꿈돌이", "호돌이"],
        3
    ),
    Quiz(
        "대전광역시를 구성하고 있는 자치구의 총 개수는 몇 개일까요?",
        ["3개", "4개", "5개", "6개"],
        3
    ),
    Quiz(
        "대전역 및 중앙로 일원에서 개최되는 대표적인 여름 축제 이름은 무엇인가요?",
        ["대전 한여름 음악제", "대전 0시 축제", "대전 불빛축제", "대전 사이언스 페스티벌"],
        2
    )
]

# Quiz game function
def play_quiz(quizzes):
    correct_count = 0

    for quiz in quizzes:
        print()
        quiz.display()
        print()

        user_answer = get_valid_number(
            "정답 번호를 입력하세요: ", 1, 4
        )

        if quiz.check_answer(user_answer):
            print("정답입니다!")
            correct_count += 1
        else:
            print("오답입니다.")

    print()
    print(f"총 {len(quizzes)}문제 중 {correct_count}문제 정답입니다!")

    return correct_count


# Add quiz function
def add_quiz(quizzes):
    question = input("새로운 퀴즈 질문을 입력하세요: ")
    print("입력한 질문:", question)


    choices = []

    for i in range(1, 5):
        choice = input(f"{i}번 보기 입력: ")
        choices.append(choice)

    print("입력한 보기:", choices)

    answer = get_valid_number("정답 번호를 입력하세요 (1~4): ", 1, 4)
    print("입력한 정답:", answer)

    new_quiz = Quiz(question, choices, answer)
    quizzes.append(new_quiz)
    print("새로운 퀴즈가 생성되었습니다!")


# Quiz list function
def show_quizzes(quizzes):
    print("\n===== 퀴즈 목록 =====")

    for i, quiz in enumerate(quizzes, start=1):
        print(f"{i}. {quiz.question}")

    print(f"\n총 {len(quizzes)}개의 퀴즈가 있습니다.")


# Main program
try:
    while True:
        print("\n===== 파이썬 퀴즈 게임 =====")
        print()
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 확인")
        print("5. 종료")
        print()
        print("※ Ctrl+C를 누르면 프로그램을 종료할 수 있습니다.")
        print()

        choice = get_valid_number("원하는 메뉴 번호를 선택하세요: ", 1, 5)

        if choice == 5:
            print("프로그램을 종료합니다.")
            break

        elif choice == 1:
            play_quiz(quizzes)

        elif choice == 2:
            add_quiz(quizzes)

        elif choice == 3:
            show_quizzes(quizzes)

        elif choice == 4:
            print("최고 점수 기능은 아직 구현되지 않았습니다.")

except KeyboardInterrupt:
    print("\n사용자 요청으로 프로그램을 종료합니다.")

except EOFError:
    print("\n입력이 종료되어 프로그램을 종료합니다.")