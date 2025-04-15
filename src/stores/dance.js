import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDanceStore = defineStore('dance', () => {
  const currentLesson = ref(null)
  const userProgress = ref({
    completedLessons: [],
    currentLevel: 'beginner',
    totalPracticeTime: 0,
    achievements: []
  })
  
  const lessonHistory = ref([])

  const setCurrentLesson = (lesson) => {
    currentLesson.value = lesson
  }

  const updateProgress = (lessonId) => {
    if (!userProgress.value.completedLessons.includes(lessonId)) {
      userProgress.value.completedLessons.push(lessonId)
    }
  }

  const addPracticeTime = (minutes) => {
    userProgress.value.totalPracticeTime += minutes
  }

  const addAchievement = (achievement) => {
    userProgress.value.achievements.push(achievement)
  }

  return {
    currentLesson,
    userProgress,
    lessonHistory,
    setCurrentLesson,
    updateProgress,
    addPracticeTime,
    addAchievement
  }
}) 