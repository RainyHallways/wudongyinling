from .base import RepositoryBase
from .user import UserRepository
from .course import CourseRepository
from .health import HealthRepository
from .prescription import (
    PrescriptionRepository, 
    PrescriptionExerciseRepository
)
from .challenge import (
    ChallengeRepository, 
    ChallengeParticipantRepository, 
    ChallengeRecordRepository
)
from .chat import (
    ChatMessageRepository, 
    ChatRoomRepository, 
    ChatRoomMemberRepository
)

# 创建单例实例
user_repository = UserRepository()
course_repository = CourseRepository()
health_repository = HealthRepository()
prescription_repository = PrescriptionRepository()
prescription_exercise_repository = PrescriptionExerciseRepository()
challenge_repository = ChallengeRepository()
challenge_participant_repository = ChallengeParticipantRepository()
challenge_record_repository = ChallengeRecordRepository()
chat_message_repository = ChatMessageRepository()
chat_room_repository = ChatRoomRepository()
chat_room_member_repository = ChatRoomMemberRepository() 