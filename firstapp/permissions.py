from .custom_user import WatchedList, Lesson, Sections
from rest_framework.permissions import BasePermission


class LessonPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        slug = view.kwargs.get('slug')
        if not slug:
            return False

        if request.user.is_staff:
            return True

        try:
            lesson = Lesson.objects.get(slug=slug)
        except Lesson.DoesNotExist:
            return False

        # `sections` maydonini to'g'ri tekshirish
        try:
            user_watchlist = WatchedList.objects.get(user=request.user, sections=lesson.section.order)
        except WatchedList.DoesNotExist:
            user_watchlist = None

        if user_watchlist is None:
            # Agar `lesson.order` raqam bo'lsa, `WatchedList` ni yaratamiz
            if lesson.order == 1:
                watch = WatchedList.objects.create(
                    user=request.user,
                    sections=lesson.section.order,
                    lessons=lesson.order
                )
                watch.save()
                return True
        elif user_watchlist:
            # `lessons` maydonining qiymatini tekshirib ko'ring
            if lesson.order - 1 == user_watchlist.lessons:
                user_watchlist.lessons = lesson.order
                user_watchlist.save()
                return True

        return False
