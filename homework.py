class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        val = (f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.'
               )
        return val


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
        pass

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

    # def __init__(self,
    #              action: int,
    #              duration: float,
    #              weight: float,
    #              ) -> None:
    #     super().__init__(action, duration, weight)

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
        cal_cff_1 = 0.035
        cal_cff_2 = 2
        cal_cff_3 = 0.029
        val = (
            (cal_cff_1 * self.weight
                + (self.get_mean_speed() ** cal_cff_2 // self.height)
                * cal_cff_3 * self.weight) * self.duration * 60)
        return val


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        val = (self.length_pool * self.count_pool
               / Training.M_IN_KM / self.duration)
        return val

    def get_spent_calories(self) -> float:
        cal_cff_1 = 1.1
        cal_cff_2 = 2
        val = (self.get_mean_speed() + cal_cff_1) * cal_cff_2 * self.weight
        return val


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_names = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    # if (len(data) == 3) and (workout_type == 'RUN'):
    #     val = class_ids[workout_type](
    #         action=data[0],
    #         duration=data[1],
    #         weight=data[2])
    # elif (len(data) == 4) and (workout_type == 'WLK'):
    #     val = class_ids[workout_type](
    #         action=data[0],
    #         duration=data[1],
    #         weight=data[2],
    #         height=data[3])
    # elif (len(data) == 5) and (workout_type == 'SWM'):
    #     val = class_ids[workout_type](
    #         action=data[0],
    #         duration=data[1],
    #         weight=data[2],
    #         length_pool=data[3],
    #         count_pool=data[4])
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
