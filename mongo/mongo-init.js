// Switch to the target database context.
db = db.getSiblingDB('group4db');

// Event metadata is stored separately from the relational event record.
db.createCollection('event_content');
db.event_content.createIndex({ eventId: 1 }, { unique: true });

// Link each document to an existing PostgreSQL event using its UUID.
db.event_content.insertMany([
    {
        eventId: UUID('20000000-0000-4000-8000-000000000001'),
        Description: {
            summary: 'An evening of emerging independent artists and local music makers.',
            ageRestriction: 'All ages',
            accessibility: ['Wheelchair accessible', 'Assistive listening devices available']
        },
        Speakers: [
            { name: 'Maya Chen', role: 'Singer-songwriter', topic: 'Building an independent music career' },
            { name: 'The Northstar Collective', role: 'Featured performers', topic: 'Live performance' }
        ],
        Schedule: [
            { startTime: '18:00', endTime: '19:00', title: 'Doors open', type: 'arrival' },
            { startTime: '19:00', endTime: '20:00', title: 'Artist showcase', type: 'performance' },
            { startTime: '20:30', endTime: '22:00', title: 'Indie Sounds Live', type: 'concert' }
        ],
        Reviews: [
            { reviewer: 'Alex Rivera', rating: 5, comment: 'A great showcase of new local talent.' },
            { reviewer: 'Jordan Lee', rating: 4, comment: 'Excellent sound and a relaxed atmosphere.' }
        ],
        Tags: ['indie', 'live-music', 'local-artists', 'concert']
    },
    {
        eventId: UUID('20000000-0000-4000-8000-000000000002'),
        Description: {
            summary: 'A night of stand-up comedy from local performers.',
            ageRestriction: '18+',
            language: 'English'
        },
        Speakers: [
            { name: 'Priya Shah', role: 'Headliner', topic: 'Observational comedy' },
            { name: 'Marcus Green', role: 'Opening comedian', topic: 'Everyday absurdities' }
        ],
        Schedule: [
            { startTime: '19:00', endTime: '19:30', title: 'Doors open', type: 'arrival' },
            { startTime: '19:30', endTime: '20:15', title: 'Opening set', type: 'comedy' },
            { startTime: '20:30', endTime: '22:00', title: 'Headliner set', type: 'comedy' }
        ],
        Reviews: [
            { reviewer: 'Sam Patel', rating: 5, comment: 'Fast-paced and genuinely funny.' }
        ],
        Tags: ['comedy', 'stand-up', 'nightlife', '18-plus']
    },
    {
        eventId: UUID('20000000-0000-4000-8000-000000000003'),
        Description: {
            summary: 'A contemporary theater production exploring family and memory.',
            ageRestriction: '12+',
            contentAdvisories: ['Flashing lights', 'Themes of grief']
        },
        Speakers: [
            { name: 'Elena Torres', role: 'Director', topic: 'Contemporary theater' },
            { name: 'David Kim', role: 'Playwright', topic: 'The Winter Play' }
        ],
        Schedule: [
            { startTime: '18:30', endTime: '19:15', title: 'Lobby reception', type: 'reception' },
            { startTime: '19:30', endTime: '21:30', title: 'The Winter Play', type: 'performance' },
            { startTime: '21:45', endTime: '22:15', title: 'Talkback with the cast', type: 'discussion' }
        ],
        Reviews: [
            { reviewer: 'Jordan Lee', rating: 5, comment: 'Thoughtful performances and beautiful staging.' },
            { reviewer: 'Alex Rivera', rating: 4, comment: 'Moving production with a strong ensemble.' }
        ],
        Tags: ['theater', 'play', 'contemporary', 'drama']
    }
]);

// The same collection also supports insertOne for individual event documents.
db.event_content.insertOne({
    eventId: UUID('20000000-0000-4000-8000-000000000004'),
    Description: {
        summary: 'A full-day outdoor festival combining live music, food, and community activities.',
        ageRestriction: 'All ages',
        amenities: ['Food vendors', 'Family area', 'Free water stations']
    },
    Speakers: [
        { name: 'The Valley Brass', role: 'Festival performers', topic: 'Live music' },
        { name: 'Northridge Food Collective', role: 'Community partners', topic: 'Local food' }
    ],
    Schedule: [
        { startTime: '11:00', endTime: '12:00', title: 'Community yoga', type: 'activity' },
        { startTime: '12:30', endTime: '15:00', title: 'Food and artist market', type: 'market' },
        { startTime: '16:00', endTime: '20:00', title: 'Main stage performances', type: 'concert' }
    ],
    Reviews: [
        { reviewer: 'Sam Patel', rating: 4, comment: 'A fun festival with plenty to explore.' }
    ],
    Tags: ['festival', 'outdoors', 'family-friendly', 'food', 'live-music']
});
