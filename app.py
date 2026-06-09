from flask import Flask, render_template, request, jsonify
from database import db, Training
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trainings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# таблицы при первом запуске
with app.app_context():
    db.create_all()


# Функция для расчёта калорий
def calculate_calories(sport_type, duration, distance=None):
    if sport_type == 'run':
        # бег: 60 ккал на 1 км
        return int(distance * 60) if distance else duration * 8
    elif sport_type == 'swim':
        # плавание: 8 ккал в минуту
        return duration * 8
    else:  # gym
        # силовая: 5 ккал в минуту
        return duration * 5


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_training', methods=['POST'])
def add_training():
    data = request.get_json()

    sport_type = data.get('sport_type')
    duration = int(data.get('duration'))
    distance = float(data.get('distance')) if data.get('distance') else None
    intensity = int(data.get('intensity')) if data.get('intensity') else None

    calories = calculate_calories(sport_type, duration, distance)

    training = Training(
        sport_type=sport_type,
        duration=duration,
        distance=distance,
        intensity=intensity,
        calories=calories
    )

    db.session.add(training)
    db.session.commit()

    return jsonify({'status': 'ok', 'message': 'Тренировка добавлена!'})


@app.route('/stats')
def stats():
    # Статистика за последние 7 дней
    week_ago = datetime.utcnow() - timedelta(days=7)
    trainings = Training.query.filter(Training.date >= week_ago).order_by(Training.date).all()

    # Группируем по дням
    days = []
    distances = []
    calories_total = 0

    for i in range(7):
        day = (datetime.utcnow() - timedelta(days=i)).strftime('%Y-%m-%d')
        days.insert(0, day)
        distances.insert(0, 0)

    for t in trainings:
        day_str = t.date.strftime('%Y-%m-%d')
        if day_str in days:
            idx = days.index(day_str)
            if t.distance:
                distances[idx] += t.distance
        calories_total += t.calories

    total_trainings = Training.query.count()
    total_distance = db.session.query(db.func.sum(Training.distance)).scalar() or 0

    return jsonify({
        'days': days,
        'distances': distances,
        'total_trainings': total_trainings,
        'total_distance': round(total_distance, 1),
        'total_calories': calories_total
    })


if __name__ == '__main__':
    app.run(debug=True)