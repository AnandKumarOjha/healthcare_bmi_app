from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            # Retrieve inputs from HTML form
            weight = float(request.form.get('weight'))
            height_cm = float(request.form.get('height'))
            age = int(request.form.get('age'))
            gender = request.form.get('gender')
            activity = float(request.form.get('activity'))

            # 1. BMI Calculation
            height_m = height_cm / 100
            bmi = round(weight / (height_m ** 2), 2)

            # Determine BMI Category
            if bmi < 18.5:
                category = "Underweight"
                category_class = "warning"
            elif 18.5 <= bmi < 24.9:
                category = "Normal Weight"
                category_class = "success"
            elif 25 <= bmi < 29.9:
                category = "Overweight"
                category_class = "warning"
            else:
                category = "Obese"
                category_class = "danger"

            # 2. BMR Calculation (Mifflin-St Jeor Equation)
            if gender == 'male':
                bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) + 5
            else:
                bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) - 161

            daily_calories = round(bmr * activity)

            result = {
                'bmi': bmi,
                'category': category,
                'category_class': category_class,
                'bmr': round(bmr),
                'daily_calories': daily_calories
            }
        except (ValueError, TypeError):
            result = {'error': 'Invalid input. Please enter valid numbers.'}

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)