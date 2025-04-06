import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSocialStore = defineStore('social', () => {
  const friends = ref([])
  const posts = ref([])
  const notifications = ref([])
  const activities = ref([])

  const addFriend = (friend) => {
    friends.value.push(friend)
  }

  const removeFriend = (friendId) => {
    friends.value = friends.value.filter(f => f.id !== friendId)
  }

  const createPost = (post) => {
    posts.value.unshift({
      ...post,
      id: Date.now(),
      timestamp: new Date().toISOString()
    })
  }

  const addNotification = (notification) => {
    notifications.value.unshift({
      ...notification,
      id: Date.now(),
      read: false
    })
  }

  const markNotificationAsRead = (notificationId) => {
    const notification = notifications.value.find(n => n.id === notificationId)
    if (notification) {
      notification.read = true
    }
  }

  const addActivity = (activity) => {
    activities.value.unshift({
      ...activity,
      id: Date.now(),
      timestamp: new Date().toISOString()
    })
  }

  return {
    friends,
    posts,
    notifications,
    activities,
    addFriend,
    removeFriend,
    createPost,
    addNotification,
    markNotificationAsRead,
    addActivity
  }
}) 