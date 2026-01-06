import { createFileRoute } from '@tanstack/react-router'
import StudentAnalyzer from '../pages/StudentAnalyzer'

export const Route = createFileRoute('/student')({
    component: StudentAnalyzer,
})
