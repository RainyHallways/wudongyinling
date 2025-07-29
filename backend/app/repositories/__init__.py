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
from .social import (
    PostRepository,
    PostCommentRepository,
    PostLikeRepository,
    HeritageProjectRepository,
    HeritageInheritorRepository
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
post_repository = PostRepository()
post_comment_repository = PostCommentRepository()
post_like_repository = PostLikeRepository()
heritage_project_repository = HeritageProjectRepository()
heritage_inheritor_repository = HeritageInheritorRepository() 