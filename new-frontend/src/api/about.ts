import request from '@/utils/request'

export interface TeamMember {
  id: string
  name: string
  title: string
  avatar: string
  description: string
}

export interface Milestone {
  id: string
  year: string
  title: string
  content: string
}

export interface Partner {
  id: string
  name: string
  logo: string
}

export function getTeamMembers() {
  return request({
    url: '/api/about/team-members',
    method: 'get'
  })
}

export function getMilestones() {
  return request({
    url: '/api/about/milestones',
    method: 'get'
  })
}

export function getPartners() {
  return request({
    url: '/api/about/partners',
    method: 'get'
  })
} 