
# Quiz Game

import json
from pathlib import Path


# 숫자 입력 검증 함수
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


# 빈 문자열 입력 검증 함수
def get_valid_text(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("내용을 입력해야 합니다.")


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


# QuizGame class
class QuizGame:
    def __init__(self):
        self.state_file = Path(__file__).with_name("state.json")
        self.best_score = 0

        self.quizzes = [
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

        self.load_state()

    # 점수 계산
    def calculate_score(self, correct_count, total_count):
        if total_count == 0:
            return 0

        return int(correct_count / total_count * 100 + 0.5)

    # JSON 파일 저장
    def save_state(self):
        data = {
            "best_score": self.best_score,
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer
                }
                for quiz in self.quizzes
            ]
        }

        try:
            with self.state_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print("게임 데이터가 저장되었습니다.")

        except OSError as error:
            print(f"데이터 저장 중 오류가 발생했습니다: {error}")

    # JSON 파일 불러오기
    def load_state(self):
        if not self.state_file.exists():
            print("저장된 데이터가 없어 기본 퀴즈를 사용합니다.")
            self.save_state()
            return

        try:
            with self.state_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("저장 데이터 형식이 올바르지 않습니다.")

            best_score = data["best_score"]
            quiz_data = data["quizzes"]

            if type(best_score) is not int or not 0 <= best_score <= 100:
                raise ValueError("최고 점수 데이터가 올바르지 않습니다.")

            if not isinstance(quiz_data, list):
                raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")

            loaded_quizzes = []

            for item in quiz_data:
                question = item["question"]
                choices = item["choices"]
                answer = item["answer"]

                if (
                    not isinstance(question, str)
                    or not question.strip()
                    or not isinstance(choices, list)
                    or len(choices) != 4
                    or not all(
                        isinstance(choice, str) and choice.strip()
                        for choice in choices
                    )
                    or type(answer) is not int
                    or not 1 <= answer <= 4
                ):
                    raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.")

                loaded_quizzes.append(Quiz(question, choices, answer))

            self.best_score = best_score
            self.quizzes = loaded_quizzes

            print("저장된 게임 데이터를 불러왔습니다.")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError, OSError) as error:
            print(f"저장 데이터에 문제가 있습니다: {error}")
            print("기본 퀴즈 데이터로 복구합니다.")

            self.best_score = 0
            self.quizzes = self.get_default_quizzes()
            self.save_state()

    # 기본 퀴즈 데이터
    def get_default_quizzes(self):
        return [
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

    # 퀴즈 출제
    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        correct_count = 0

        for quiz in self.quizzes:
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

        total_count = len(self.quizzes)
        score = self.calculate_score(correct_count, total_count)

        print(
            f"이번 점수: {score}점 "
            f"({total_count}문제 중 {correct_count}문제 정답입니다!)"
        )

        if score > self.best_score:
            self.best_score = score
            print("축하합니다! 최고 점수가 갱신되었습니다!")
            self.save_state()

    # 퀴즈 추가
    def add_quiz(self):
        question = get_valid_text("새로운 퀴즈 질문을 입력하세요: ")

        choices = []

        for i in range(1, 5):
            choice = get_valid_text(f"{i}번 보기 입력: ")
            choices.append(choice)

        answer = get_valid_number(
            "정답 번호를 입력하세요 (1~4): ", 1, 4
        )

        print("\n===== 입력 내용 확인 =====")
        print("질문:", question)

        for i, choice in enumerate(choices, start=1):
            print(f"{i}번 보기: {choice}")

        print("입력한 정답 번호:", answer)
        print("정답 내용:", choices[answer - 1])

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)

        print("\n새로운 퀴즈가 생성되었습니다!")
        self.save_state()

    # 퀴즈 목록
    def show_quizzes(self):
        print("\n===== 퀴즈 목록 =====")

        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"{i}. {quiz.question}")

        print(f"\n총 {len(self.quizzes)}개의 퀴즈가 있습니다.")

    # 최고 점수 확인
    def show_best_score(self):
        print(f"\n현재 최고 점수: {self.best_score}점")

    # 메인 메뉴
    def run(self):
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

                choice = get_valid_number(
                    "원하는 메뉴 번호를 선택하세요: ", 1, 5
                )

                if choice == 5:
                    print("프로그램을 종료합니다.")
                    break

                elif choice == 1:
                    self.play()

                elif choice == 2:
                    self.add_quiz()

                elif choice == 3:
                    self.show_quizzes()

                elif choice == 4:
                    self.show_best_score()

        except KeyboardInterrupt:
            print("\n사용자 요청으로 프로그램을 종료합니다.")

        except EOFError:
            print("\n입력이 종료되어 프로그램을 종료합니다.")


# 게임 실행
if __name__ == "__main__":
    game = QuizGame()
    game.run()
