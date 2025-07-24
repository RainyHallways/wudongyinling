import { request } from '../utils/request'

// 社交动态接口
export interface Post {
  id: number
  user_id: number
  user_name: string
  user_avatar?: string
  content: string
  images?: string[]
  video_url?: string
  like_count: number
  comment_count: number
  share_count: number
  is_liked?: boolean
  created_at: string
  tags?: string[]
}

// 评论接口
export interface Comment {
  id: number
  post_id: number
  user_id: number
  user_name: string
  user_avatar?: string
  content: string
  like_count: number
  is_liked?: boolean
  created_at: string
  parent_id?: number
  replies?: Comment[]
}

// 社区圈子接口
export interface Community {
  id: number
  name: string
  description: string
  avatar?: string
  cover?: string
  member_count: number
  post_count: number
  is_joined?: boolean
  created_at: string
  creator_id: number
  creator_name?: string
}

// 活动接口
export interface Event {
  id: number
  title: string
  description: string
  cover_image?: string
  location?: string
  start_time: string
  end_time: string
  max_participants?: number
  current_participants: number
  is_registered?: boolean
  status: 'upcoming' | 'ongoing' | 'ended'
  organizer_id: number
  organizer_name?: string
  created_at: string
}

// 用户关系接口
export interface UserRelation {
  user_id: number
  username: string
  nickname?: string
  avatar?: string
  following_count: number
  follower_count: number
  is_following?: boolean
  is_followed?: boolean
}

/**
 * 社交相关API
 */
export const socialApi = {
  /**
   * 获取社交动态列表
   * @param params 查询参数
   */
  getPosts(params?: { skip?: number, limit?: number, community_id?: number }) {
    return request.get<{ items: Post[], total: number }>('/social/posts', params)
  },
  
  /**
   * 获取社交动态详情
   * @param id 动态ID
   */
  getPostById(id: number) {
    return request.get<Post>(`/social/posts/${id}`)
  },
  
  /**
   * 创建社交动态
   * @param data 动态数据
   */
  createPost(data: {
    content: string,
    images?: File[],
    video?: File,
    community_id?: number,
    tags?: string[]
  }) {
    const formData = new FormData()
    formData.append('content', data.content)
    
    if (data.community_id) {
      formData.append('community_id', data.community_id.toString())
    }
    
    if (data.tags && data.tags.length > 0) {
      formData.append('tags', JSON.stringify(data.tags))
    }
    
    if (data.images && data.images.length > 0) {
      data.images.forEach((image, index) => {
        formData.append(`image_${index}`, image)
      })
    }
    
    if (data.video) {
      formData.append('video', data.video)
    }
    
    return request.post<Post>('/social/posts', formData)
  },
  
  /**
   * 删除社交动态
   * @param id 动态ID
   */
  deletePost(id: number) {
    return request.delete(`/social/posts/${id}`)
  },
  
  /**
   * 点赞/取消点赞动态
   * @param id 动态ID
   * @param like 是否点赞
   */
  likePost(id: number, like: boolean = true) {
    return request.post<{success: boolean}>(`/social/posts/${id}/${like ? 'like' : 'unlike'}`)
  },
  
  /**
   * 获取动态评论列表
   * @param postId 动态ID
   * @param params 查询参数
   */
  getComments(postId: number, params?: { skip?: number, limit?: number }) {
    return request.get<{ items: Comment[], total: number }>(`/social/posts/${postId}/comments`, params)
  },
  
  /**
   * 创建评论
   * @param postId 动态ID
   * @param content 评论内容
   * @param parentId 父评论ID（回复某条评论）
   */
  createComment(postId: number, content: string, parentId?: number) {
    const data = { content }
    if (parentId) {
      Object.assign(data, { parent_id: parentId })
    }
    return request.post<Comment>(`/social/posts/${postId}/comments`, data)
  },
  
  /**
   * 删除评论
   * @param commentId 评论ID
   */
  deleteComment(commentId: number) {
    return request.delete(`/social/comments/${commentId}`)
  },
  
  /**
   * 获取社区圈子列表
   * @param params 查询参数
   */
  getCommunities(params?: { skip?: number, limit?: number, search?: string }) {
    return request.get<{ items: Community[], total: number }>('/social/communities', params)
  },
  
  /**
   * 获取社区圈子详情
   * @param id 圈子ID
   */
  getCommunityById(id: number) {
    return request.get<Community>(`/social/communities/${id}`)
  },
  
  /**
   * 创建社区圈子
   * @param data 圈子数据
   */
  createCommunity(data: Partial<Community>) {
    return request.post<Community>('/social/communities', data)
  },
  
  /**
   * 更新社区圈子
   * @param id 圈子ID
   * @param data 圈子数据
   */
  updateCommunity(id: number, data: Partial<Community>) {
    return request.put<Community>(`/social/communities/${id}`, data)
  },
  
  /**
   * 加入/退出社区圈子
   * @param id 圈子ID
   * @param join 是否加入
   */
  joinCommunity(id: number, join: boolean = true) {
    return request.post<{success: boolean}>(`/social/communities/${id}/${join ? 'join' : 'leave'}`)
  },
  
  /**
   * 获取活动列表
   * @param params 查询参数
   */
  getEvents(params?: { skip?: number, limit?: number, status?: string }) {
    return request.get<{ items: Event[], total: number }>('/social/events', params)
  },
  
  /**
   * 获取活动详情
   * @param id 活动ID
   */
  getEventById(id: number) {
    return request.get<Event>(`/social/events/${id}`)
  },
  
  /**
   * 创建活动
   * @param data 活动数据
   */
  createEvent(data: Partial<Event>) {
    return request.post<Event>('/social/events', data)
  },
  
  /**
   * 更新活动
   * @param id 活动ID
   * @param data 活动数据
   */
  updateEvent(id: number, data: Partial<Event>) {
    return request.put<Event>(`/social/events/${id}`, data)
  },
  
  /**
   * 报名/取消活动
   * @param id 活动ID
   * @param register 是否报名
   */
  registerEvent(id: number, register: boolean = true) {
    return request.post<{success: boolean}>(`/social/events/${id}/${register ? 'register' : 'cancel'}`)
  },
  
  /**
   * 获取我关注的用户列表
   * @param params 查询参数
   */
  getFollowing(params?: { skip?: number, limit?: number }) {
    return request.get<{ items: UserRelation[], total: number }>('/social/user/following', params)
  },
  
  /**
   * 获取关注我的用户列表
   * @param params 查询参数
   */
  getFollowers(params?: { skip?: number, limit?: number }) {
    return request.get<{ items: UserRelation[], total: number }>('/social/user/followers', params)
  },
  
  /**
   * 关注/取消关注用户
   * @param userId 用户ID
   * @param follow 是否关注
   */
  followUser(userId: number, follow: boolean = true) {
    return request.post<{success: boolean}>(`/social/user/${userId}/${follow ? 'follow' : 'unfollow'}`)
  },
  
  /**
   * 获取用户动态
   * @param userId 用户ID
   * @param params 查询参数
   */
  getUserPosts(userId: number, params?: { skip?: number, limit?: number }) {
    return request.get<{ items: Post[], total: number }>(`/social/user/${userId}/posts`, params)
  }
} 