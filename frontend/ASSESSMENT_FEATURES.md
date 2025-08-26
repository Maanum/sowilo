# Assessment Generation Features

This document describes the assessment generation features available in the Sowilo application.

## Overview

The application now supports comprehensive assessment generation for job opportunities, with multiple ways to generate and manage assessments.

## Components

### 1. GenerateAssessmentButton

A standalone button component for generating assessments for opportunities that don't have one yet.

**Features:**

- Shows loading state while generating
- Handles errors gracefully
- Customizable styling and size
- Callback for when assessment is created

**Usage:**

```tsx
<GenerateAssessmentButton
  opportunityId={1}
  profileId={1}
  onAssessmentCreated={assessment => {
    // Handle the new assessment
  }}
  variant="outline"
  size="sm"
/>
```

### 2. AssessmentDrawer

A slide-out drawer that displays detailed assessment information and provides regeneration capabilities.

**Features:**

- Displays fit score (1-7 scale)
- Shows summary of fit and recommendations
- Indicates if assessment is outdated
- Regenerate button with loading state
- Metadata (assessment date, profile version, last updated)

**Usage:**

```tsx
<AssessmentDrawer
  currentProfileVersion={1}
  onAssessmentUpdated={assessment => {
    // Handle updated assessment
  }}
/>
```

### 3. FitScoreBadge

A compact badge that displays the fit score for opportunities with assessments.

**Features:**

- Color-coded scores (green for 6-7, yellow for 4-5, red for 1-3)
- Outdated indicator (red dot) when profile version doesn't match
- Clickable to open assessment drawer
- Shows "—" when no assessment exists

## User Interface

### Opportunity Cards

Each opportunity card now shows:

1. **Header Area:**

   - If assessment exists: Fit score badge (clickable)
   - If no assessment: "Generate Assessment" button with "No assessment" label

2. **Expanded View:**
   - Assessment section with detailed information
   - Summary of fit (truncated if too long)
   - Regenerate button for existing assessments
   - "View Details" button to open drawer
   - Last updated timestamp

### Assessment Drawer

The drawer provides:

- Large fit score display
- Complete summary and recommendations
- Outdated warning if applicable
- Regenerate button with visual feedback
- Assessment metadata

## API Integration

The assessment system integrates with the backend API:

- `GET /assessments/opportunities/{id}` - Retrieve single assessment
- `POST /assessments/opportunities/{id}/assess` - Generate/regenerate assessment

## Workflow

1. **New Opportunity:** When a new opportunity is created, it shows a "Generate Assessment" button
2. **Generate Assessment:** Clicking the button creates an assessment using the current profile
3. **View Assessment:** The fit score badge appears and is clickable to view details
4. **Regenerate Assessment:** Users can regenerate assessments from the drawer or expanded view
5. **Outdated Detection:** System detects when assessments are based on older profile versions

## Error Handling

- Network errors are logged to console
- Loading states prevent multiple simultaneous requests
- Graceful fallbacks for missing assessments

## Future Enhancements

Potential improvements:

- Toast notifications for success/error states
- Bulk assessment generation
- Assessment history tracking
- Export assessment data
- Custom assessment criteria
