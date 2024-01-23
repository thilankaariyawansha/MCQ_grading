import os
import pandas as pd

class MCQGrader:
    def answers(self, subject, yr, num_of_q):
        """Collects answers for  questions and saves them to a CSV file.

        Args:
           subject (str): The subject for which the answers are being collected.
           yr (str): The year associated with the answers.
        """

        answers_dict = {}

        for q in range(num_of_q):
            question_label = f"Q{q + 1}"
            answer = input(f"Enter correct answers for {question_label}: ")
            answers_dict[question_label] = answer

        answer_df = pd.DataFrame(answers_dict, index=[0])

        print("*******************************************")
        print(answer_df)

        print("*******************************************")
        print("Confirm to Print")
        conf = input("Confirm (Y/N) : ")

        if conf == "Y":
            csv_file = f"answers_{subject}_{yr}.csv"

            if os.path.exists(csv_file):
                existing_data = pd.read_csv(csv_file)
                mode = 'a'  # Append to existing file
                header = False  # Don't write header again
            else:
                existing_data = pd.DataFrame()
                mode = 'w'  # Create a new file
                header = True  # Write header for the first time

            pd.concat([existing_data, answer_df], ignore_index=True).to_csv(
                csv_file, index=False, mode=mode, header=header
            )
        else:
            pass

    def given_answer(self, subject, yr, student_indx):
        csv_file = f"given_answ_{subject}_{yr}.csv"
        stud_answ = pd.read_csv(csv_file)

        column1_values = stud_answ['Index'].values

        if student_indx in column1_values:
            print("This result already available")
        else:
            given_answ_dict = {"Index": student_indx}

            num_columns = 10
            for q in range(num_columns):
                question_label = f"Q{q + 1}"
                answer = input(f"Enter the given answers for {question_label}: ")
                given_answ_dict[question_label] = answer

            given_answ_df = pd.DataFrame(given_answ_dict, index=[0])

            print("*******************************************")
            print(given_answ_df)
            print("*******************************************")

            conf = input("Confirm (Y/N): ")
            if conf.upper() == "Y":
                if os.path.exists(csv_file):
                    existing_data = pd.read_csv(csv_file)
                    mode = 'a'  # Append to existing file
                    header = False  # Don't write header again
                else:
                    existing_data = pd.DataFrame()
                    mode = 'w'  # Create a new file
                    header = True  # Write header for the first time

                pd.concat([existing_data, given_answ_df], ignore_index=True).to_csv(
                    csv_file, index=False, mode=mode, header=header
                )
            else:
                print("Data not saved.")

    def check_res(self, stu_answ_file, cor_ans_file):
        stud_answ = pd.read_csv(stu_answ_file)
        correct_answers = pd.read_csv(cor_ans_file)

        ans_dic = {}
        for idx in range(correct_answers.shape[1]):
            ky = "Q" + str(idx + 1)
            ans_dic[ky] = list(correct_answers[ky][0])

        for num_of_stu in range(len(stud_answ)):
            row_data_dict = stud_answ.iloc[num_of_stu].to_dict()
            studentNum = row_data_dict["Index"]
            student_answers = {}

            totalcorrect = 0
            totalmarked = 0

            for stans in range(1, len(row_data_dict)):
                dicKy = "Q" + str(stans)
                asw = row_data_dict[dicKy]
                student_answers[dicKy] = list(str(asw)) if not isinstance(asw, float) else []

                corect_aswr_count = sum(1 for item in student_answers[dicKy] if item in ans_dic[dicKy])
                total_marked_itms = len(student_answers[dicKy])

                totalcorrect += corect_aswr_count
                totalmarked += total_marked_itms

            wrong_answ = totalmarked - totalcorrect
            net_correct = totalcorrect - wrong_answ
            percentage = (net_correct / 17) * 100

            print(
                f"{studentNum} | Corrects : {totalcorrect}, Wrongs : {wrong_answ}, Net : [{net_correct}], Total Marked : {totalmarked}, Percentage (from Net): {percentage}%"
            )


# Example usage:
# mcq_grader = MCQGrader()
# mcq_grader.answers("Math", "2023", 10)
# mcq_grader.given_answer("Math", "2023", "123")
# mcq_grader.check_res("given_answ_Math_2023.csv", "answers_Math_2023.csv")
