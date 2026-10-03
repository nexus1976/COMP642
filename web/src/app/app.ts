import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

interface EndpointField {
  name: string;
  label: string;
  location: 'path' | 'query';
  initialValue?: string;
  type?: 'text' | 'number';
  options?: string[];
  placeholder?: string;
  required?: boolean;
}

interface Endpoint {
  id: string;
  method: 'GET' | 'POST' | 'DELETE';
  path: string;
  description: string;
  fields: EndpointField[];
  bodyLabel?: string;
  bodyExample?: string;
}

interface EndpointGroup {
  name: string;
  description: string;
  endpoints: Endpoint[];
}

interface RequestResult {
  status: number;
  ok: boolean;
  elapsedMs: number;
  payload: unknown;
}

@Component({
  selector: 'app-root',
  imports: [FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  private readonly http = inject(HttpClient);

  readonly groups: EndpointGroup[] = [
    {
      name: 'Events',
      description: 'Browse events, event content, reviews, search, and trending activity.',
      endpoints: [
        {
          id: 'list-events',
          method: 'GET',
          path: '/events',
          description: 'Return all events.',
          fields: []
        },
        {
          id: 'get-event',
          method: 'GET',
          path: '/events/:id',
          description: 'Return one event. Cache is enabled by default.',
          fields: [
            { name: 'id', label: 'Event ID', location: 'path', initialValue: '20000000-0000-4000-8000-000000000001', required: true },
            { name: 'bypass_cache', label: 'Bypass Redis cache', location: 'query', initialValue: 'false', options: ['false', 'true'] }
          ]
        },
        {
          id: 'get-event-content',
          method: 'GET',
          path: '/events/:id/content',
          description: 'Return the MongoDB content document for an event.',
          fields: [
            { name: 'id', label: 'Event ID', location: 'path', initialValue: '20000000-0000-4000-8000-000000000001', required: true }
          ]
        },
        {
          id: 'create-review',
          method: 'POST',
          path: '/events/:id/reviews',
          description: 'Add a review to an event content document.',
          fields: [
            { name: 'id', label: 'Event ID', location: 'path', initialValue: '20000000-0000-4000-8000-000000000001', required: true }
          ],
          bodyLabel: 'Review JSON',
          bodyExample: JSON.stringify({ reviewer: 'Demo Reviewer', rating: 5, comment: 'Great event!' }, null, 2)
        },
        {
          id: 'delete-reviews',
          method: 'DELETE',
          path: '/events/:id/reviews/:reviewer',
          description: 'Delete all reviews by the specified reviewer for an event.',
          fields: [
            { name: 'id', label: 'Event ID', location: 'path', initialValue: '20000000-0000-4000-8000-000000000001', required: true },
            { name: 'reviewer', label: 'Reviewer name', location: 'path', placeholder: 'Reviewer name', required: true }
          ]
        },
        {
          id: 'search-tag',
          method: 'GET',
          path: '/events/search/tags/:tag',
          description: 'Search event content by tag.',
          fields: [
            { name: 'tag', label: 'Tag', location: 'path', initialValue: 'concert', required: true }
          ]
        },
        {
          id: 'search-speaker',
          method: 'GET',
          path: '/events/search/speakers/:speaker',
          description: 'Search event content by speaker name.',
          fields: [
            { name: 'speaker', label: 'Speaker name', location: 'path', placeholder: 'Speaker name', required: true }
          ]
        },
        {
          id: 'search-reviews',
          method: 'GET',
          path: '/events/search/reviews',
          description: 'Find events with a review at or above the selected rating.',
          fields: [
            { name: 'rating', label: 'Minimum rating (1-5)', location: 'query', type: 'number', initialValue: '4', required: true }
          ]
        },
        {
          id: 'search-attributes',
          method: 'GET',
          path: '/events/search/attributes',
          description: 'Search by one or more nested event attributes.',
          fields: [
            { name: 'speaker_role', label: 'Speaker role', location: 'query', placeholder: 'e.g. performer' },
            { name: 'speaker_topic', label: 'Speaker topic', location: 'query', placeholder: 'e.g. jazz' },
            { name: 'min_review_rating', label: 'Minimum review rating', location: 'query', type: 'number', placeholder: '1–5' },
            { name: 'age_restriction', label: 'Age restriction', location: 'query', placeholder: 'e.g. 18+' },
            { name: 'tag', label: 'Tag', location: 'query', placeholder: 'e.g. concert' }
          ]
        },
        {
          id: 'search-concerts',
          method: 'GET',
          path: '/events/search/concerts/genre/:genre',
          description: 'Find concerts by genre.',
          fields: [
            { name: 'genre', label: 'Genre', location: 'path', placeholder: 'e.g. jazz', required: true }
          ]
        },
        {
          id: 'trending-events',
          method: 'GET',
          path: '/trending',
          description: 'Return the top 10 trending event IDs and scores.',
          fields: []
        }
      ]
    },
    {
      name: 'Users',
      description: "List users, create a user, or retrieve a user's orders.",
      endpoints: [
        {
          id: 'list-users',
          method: 'GET',
          path: '/users',
          description: 'Return all users.',
          fields: []
        },
        {
          id: 'create-user',
          method: 'POST',
          path: '/users',
          description: 'Create a user record.',
          fields: [],
          bodyLabel: 'User JSON',
          bodyExample: JSON.stringify({
            id: '00000000-0000-4000-8000-000000000001',
            first_name: 'Demo',
            last_name: 'User',
            email: 'demo@example.com',
            password: 'replace-this-demo-password',
            username: 'demo_user',
            isadmin: false
          }, null, 2)
        },
        {
          id: 'user-orders',
          method: 'GET',
          path: '/users/:id/orders',
          description: 'Return orders associated with a user ID.',
          fields: [
            { name: 'id', label: 'User ID', location: 'path', placeholder: 'UUID', required: true }
          ]
        }
      ]
    },
    {
      name: 'Orders',
      description: 'Create an order or look one up by ID.',
      endpoints: [
        {
          id: 'create-order',
          method: 'POST',
          path: '/orders',
          description: 'Create an order and its order items in a transaction.',
          fields: [],
          bodyLabel: 'Order JSON',
          bodyExample: JSON.stringify({
            id: '00000000-0000-0000-0000-000000000000',
            user_id: '00000000-0000-4000-8000-000000000001',
            event_id: '20000000-0000-4000-8000-000000000001',
            total_amount: 0,
            status: 'pending',
            order_items: []
          }, null, 2)
        },
        {
          id: 'get-order',
          method: 'GET',
          path: '/orders/:id',
          description: 'Return an order and its items.',
          fields: [
            { name: 'id', label: 'Order ID', location: 'path', placeholder: 'UUID', required: true }
          ]
        }
      ]
    },
    {
      name: 'Database',
      description: 'Run a SQL query using the backend SQL demonstration endpoint.',
      endpoints: [
        {
          id: 'execute-sql',
          method: 'POST',
          path: '/executesql',
          description: 'The SQL is sent to the database as entered. Use only queries you intend to run.',
          fields: [],
          bodyLabel: 'Request JSON',
          bodyExample: JSON.stringify({ sql: 'SELECT 1 AS ok;' }, null, 2)
        }
      ]
    }
  ];

  readonly fieldValues = this.createFieldValues();
  readonly bodyValues = this.createBodyValues();
  readonly results = signal<Record<string, RequestResult>>({});
  readonly loadingEndpoint = signal<string | null>(null);

  callEndpoint(endpoint: Endpoint): void {
    let url: string;
    let body: unknown;
    try {
      ({ url, body } = this.buildRequest(endpoint));
    } catch (error) {
      this.saveResult(endpoint.id, {
        status: 0,
        ok: false,
        elapsedMs: 0,
        payload: { error: error instanceof Error ? error.message : String(error) }
      });
      return;
    }

    const startedAt = performance.now();
    this.loadingEndpoint.set(endpoint.id);
    this.http.request(endpoint.method, url, {
      body,
      observe: 'response',
      responseType: 'text'
    }).subscribe({
      next: (response) => {
        this.saveResult(endpoint.id, {
          status: response.status,
          ok: response.ok,
          elapsedMs: Number((performance.now() - startedAt).toFixed(1)),
          payload: this.parseResponse(response.body ?? '')
        });
        this.loadingEndpoint.set(null);
      },
      error: (error: HttpErrorResponse) => {
        this.saveResult(endpoint.id, {
          status: error.status,
          ok: false,
          elapsedMs: Number((performance.now() - startedAt).toFixed(1)),
          payload: this.parseResponse(error.error)
        });
        this.loadingEndpoint.set(null);
      }
    });
  }

  formatPayload(payload: unknown): string {
    if (typeof payload === 'string') {
      return payload;
    }
    return JSON.stringify(payload, null, 2) ?? String(payload);
  }

  private buildRequest(endpoint: Endpoint): { url: string; body?: unknown } {
    let path = endpoint.path;
    const query = new URLSearchParams();

    for (const field of endpoint.fields) {
      const value = (this.fieldValues[endpoint.id]?.[field.name] ?? '').trim();
      if (!value && field.required) {
        throw new Error(`${field.label} is required.`);
      }
      if (!value) {
        continue;
      }
      if (field.location === 'path') {
        path = path.replace(`:${field.name}`, encodeURIComponent(value));
      } else {
        query.set(field.name, value);
      }
    }

    let body: unknown;
    if (endpoint.bodyLabel) {
      const bodyText = this.bodyValues[endpoint.id]?.trim() ?? '';
      if (!bodyText) {
        throw new Error('A JSON request body is required.');
      }
      try {
        body = JSON.parse(bodyText) as unknown;
      } catch {
        throw new Error('The request body must be valid JSON.');
      }
    }

    const queryString = query.toString();
    return {
      url: `/api${path}${queryString ? `?${queryString}` : ''}`,
      body
    };
  }

  private parseResponse(text: string): unknown {
    if (!text) {
      return '';
    }
    try {
      return JSON.parse(text) as unknown;
    } catch {
      return text;
    }
  }

  private saveResult(endpointId: string, result: RequestResult): void {
    this.results.update((current) => ({ ...current, [endpointId]: result }));
  }

  private createFieldValues(): Record<string, Record<string, string>> {
    const values: Record<string, Record<string, string>> = {};
    for (const group of this.groups) {
      for (const endpoint of group.endpoints) {
        values[endpoint.id] = Object.fromEntries(
          endpoint.fields.map((field) => [field.name, field.initialValue ?? ''])
        );
      }
    }
    return values;
  }

  private createBodyValues(): Record<string, string> {
    const values: Record<string, string> = {};
    for (const group of this.groups) {
      for (const endpoint of group.endpoints) {
        if (endpoint.bodyExample) {
          values[endpoint.id] = endpoint.bodyExample;
        }
      }
    }
    return values;
  }
}
