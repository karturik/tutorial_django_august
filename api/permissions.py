from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет читать всем, 
    а изменять - только персоналу (is_staff=True).
    """
    def has_permission(self, request, view):
        # Разрешить GET, HEAD, OPTIONS запросы всем
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Разрешить запись только пользователям с флагом is_staff
        # request.user должен существовать и быть аутентифицированным 
        # (это обычно проверяется классом аутентификации до разрешения)
        return request.user and request.user.is_staff 

# --- Можно добавить и IsOwnerOrReadOnly, если у моделей есть поле owner ---
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение позволяет редактировать объект только его владельцу.
    Предполагает, что у модели есть поле 'owner'.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешения на чтение разрешены всем,
        # поэтому мы всегда разрешаем GET, HEAD или OPTIONS запросы.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешения на запись предоставляются только владельцу объекта.
        # Убедитесь, что у объекта `obj` есть атрибут `owner`!
        # return obj.owner == request.user 
        # В наших моделях catalog нет owner, поэтому это просто пример.
        # Если бы owner был, нужно было бы раскомментировать строку выше.
        # Пока вернем False для небезопасных методов, если owner не совпадает.
        # Или можно вернуть проверку на is_staff, как временную меру:
        return request.user and request.user.is_staff