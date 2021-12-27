from dataclasses import dataclass

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MSG_TMPLT = ('Тип тренировки: {}; Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.MSG_TMPLT.format(self.training_type,
            self.duration, self.distance, self.speed, 
            self.calories)


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65

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
        raise(NotImplementedError('Метод get_spent_calories не определен'))

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
        SPD_MULT = 18
        SPD_DIFF = 20
        return ((SPD_MULT * self.get_mean_speed()
                - SPD_DIFF) * self.weight
            / self.M_IN_KM * self.duration * 60)


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
        WGHT_MULT1 = 0.035
        SPD_POW = 2
        WGHT_MULT2 = 0.029
        val = (
            (WGHT_MULT1 * self.weight
                + (self.get_mean_speed() ** SPD_POW // self.height)
                * WGHT_MULT2 * self.weight) * self.duration * 60)
        return val


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
        val = (self.length_pool * self.count_pool
               / self.M_IN_KM / self.duration)
        return val

    def get_spent_calories(self) -> float:
        SPD_SUM_COEF = 1.1
        WEIGHT_MULT = 2
        val = (self.get_mean_speed() + SPD_SUM_COEF) * WEIGHT_MULT * self.weight
        return val


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_names = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type not in class_names.keys():
        raise(ValueError('Тип тренировки не определен'))
    else:
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
