from .models import Area, Factory


def validate_factory(factory: Factory) -> list[str]:
    errors = []

    if factory.width_m <= 0:
        errors.append("工場の横幅は0より大きい値を入力してください。")

    if factory.height_m <= 0:
        errors.append("工場の縦幅は0より大きい値を入力してください。")

    return errors


def validate_area(area: Area) -> list[str]:
    errors = []

    if not area.id:
        errors.append("設備IDを入力してください。")

    if not area.name:
        errors.append("設備名を入力してください。")

    if area.count <= 0:
        errors.append("設備数は1以上を入力してください。")

    if area.width_m <= 0:
        errors.append("設備の幅は0より大きい値を入力してください。")

    if area.height_m <= 0:
        errors.append("設備の奥行きは0より大きい値を入力してください。")

    return errors