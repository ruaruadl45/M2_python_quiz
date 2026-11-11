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


try:
    print("===== 파이썬 퀴즈 게임 =====")
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
    else:
        print("선택한 번호:", choice)

except KeyboardInterrupt:
    print("\n사용자 요청으로 프로그램을 종료합니다.")

except EOFError:
    print("\n입력이 종료되어 프로그램을 종료합니다.")

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

