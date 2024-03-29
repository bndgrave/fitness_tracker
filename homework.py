from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    OUT_MESSAGE = (
        'Тип тренировки: {training_type}; Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.OUT_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод get_spent_calories не определен')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        SPEED_MULT = 18
        SPEED_DIFF = 20
        return (
            (SPEED_MULT * self.get_mean_speed()
                - SPEED_DIFF) * self.weight
            / self.M_IN_KM * self.duration * self.MIN_IN_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        WEIGHT_MULT1 = 0.035
        WEIGHT_MULT2 = 0.029
        return (
            (WEIGHT_MULT1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * WEIGHT_MULT2 * self.weight) * self.duration
            * self.MIN_IN_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        val = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )
        return val

    def get_spent_calories(self) -> float:
        SPD_SUM_COEF = 1.1
        WEIGHT_MULT = 2
        return (
            (self.get_mean_speed() + SPD_SUM_COEF)
            * WEIGHT_MULT * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_names = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type not in class_names:
        raise ValueError('Тип тренировки не определен')
    return class_names[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
