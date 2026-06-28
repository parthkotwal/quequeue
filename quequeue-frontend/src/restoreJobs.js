import apiClient from './api'

const TERMINAL_STATUSES = new Set(['succeeded', 'partial_failed', 'failed'])

function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

export async function startRestoreJob(queueId) {
  const { data } = await apiClient.post(`/queue/${queueId}/restore/`)
  return data.job
}

export async function waitForRestoreJob(jobId, { onUpdate } = {}) {
  let pendingAttempts = 0
  for (let attempt = 0; attempt < 300; attempt += 1) {
    const { data } = await apiClient.get(`/restore_jobs/${jobId}/`)
    const job = data.job
    if (onUpdate) onUpdate(job)
    if (TERMINAL_STATUSES.has(job.status)) {
      return job
    }
    if (job.status === 'pending') {
      pendingAttempts += 1
      if (pendingAttempts >= 15) {
        throw new Error('Restore job is queued, but no worker has picked it up yet.')
      }
    } else {
      pendingAttempts = 0
    }
    await wait(1000)
  }

  throw new Error('Restore job timed out')
}

export function restoreErrorMessage(job) {
  if (job.error === 'NO_ACTIVE_DEVICE') {
    return 'Please start playback in Spotify first, then try restoring the queue.'
  }
  return job.error || 'Restore job failed.'
}
