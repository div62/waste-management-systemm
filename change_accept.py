"""
One-time update for gui.py: service providers also see accepted requests whose
collection was deleted, and they can accept those again.
Run once from the BinGO folder with: python change_accept_logic.py
Then delete this file.
"""
import os
import shutil

FOLDER = os.path.dirname(os.path.abspath(__file__))
GUI_PATH = os.path.join(FOLDER, "gui.py")

ACCEPT_START = "    def get_provider_city(self):\n"
ACCEPT_END = "    def mark_selected_collected(self):\n"
FILTER_START = "            # Service providers see only pending requests from their own city.\n"
FILTER_END = "            # Search every displayed column without changing the saved database data.\n"

NEW_ACCEPT_METHODS = r'''    def get_provider_city(self):
        """Return the city ID saved on this service provider's profile."""
        connection = get_connection()
        row = connection.execute(
            "SELECT city_id FROM providers WHERE id = ?", (self.linked_id,)
        ).fetchone()
        connection.close()
        return row[0] if row else None

    def get_linked_request_ids(self):
        """Return the request IDs that already have a collection."""
        connection = get_connection()
        rows = connection.execute(
            'SELECT "request_id" FROM "waste_collections" WHERE "request_id" IS NOT NULL'
        ).fetchall()
        connection.close()
        return {row[0] for row in rows}

    def accept_selected_request(self):
        """Accept a pending request, or an accepted one whose collection was deleted."""
        if self.selected_record is None:
            messagebox.showwarning("Select a Request", "Click a request row first, then click Accept Request.")
            return

        columns = MODULES["Requests"][1]
        request_id = self.selected_record[columns.index("id")]
        waste_type = self.selected_record[columns.index("waste_type")]
        quantity = self.selected_record[columns.index("quantity")]
        city_id = self.selected_record[columns.index("city_id")]
        area_id = self.selected_record[columns.index("area_id")]
        preferred_date = self.selected_record[columns.index("preferred_date")]
        status = self.selected_record[columns.index("status")]
        if status not in ("Pending", "Accepted"):
            messagebox.showwarning("Not Available", "This request can't be accepted.")
            return

        collection_id = generate_id("waste_collections")
        connection = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            # Accept only if the request is Pending, or Accepted with no collection left.
            # The check and the update happen together, so two providers can't both win.
            cursor.execute(
                'UPDATE "requests" SET "status" = ? WHERE "id" = ? AND ("status" = ? OR '
                '("status" = ? AND "id" NOT IN (SELECT "request_id" FROM "waste_collections" '
                'WHERE "request_id" IS NOT NULL)))',
                ("Accepted", request_id, "Pending", "Accepted"),
            )
            if cursor.rowcount == 0:
                connection.rollback()
                messagebox.showwarning("Not Available", "Another provider already accepted this request.")
            else:
                cursor.execute(
                    'INSERT INTO "waste_collections" ("id", "waste_type", "quantity", "city_id", '
                    '"area_id", "provider_id", "collection_date", "status", "request_id") '
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (collection_id, waste_type, quantity, city_id, area_id,
                     self.linked_id, preferred_date, "Assigned", request_id),
                )
                connection.commit()
                messagebox.showinfo("Accepted", "Request " + request_id + " accepted. Collection " + collection_id + " was created.")
        except sqlite3.Error as error:
            if connection is not None:
                connection.rollback()
            messagebox.showerror("Database Error", "Could not accept the request:\n" + str(error))
        finally:
            if connection is not None:
                connection.close()

        self.selected_record = None
        self.show_module("Requests")

'''

NEW_FILTER = r'''            # Service providers see pending requests from their city, plus accepted requests
            # whose collection was deleted, so those can be accepted again.
            if self.role == "Service Provider" and page_name == "Requests":
                city_index = columns.index("city_id")
                status_index = columns.index("status")
                id_index = columns.index("id")
                provider_city = self.get_provider_city()
                linked_ids = self.get_linked_request_ids()
                rows = [
                    row for row in rows
                    if row[city_index] == provider_city
                    and (row[status_index] == "Pending"
                         or (row[status_index] == "Accepted" and row[id_index] not in linked_ids))
                ]

'''


def main():
    with open(GUI_PATH, encoding="utf-8") as gui_file:
        text = gui_file.read()

    markers = [ACCEPT_START, ACCEPT_END, FILTER_START, FILTER_END]
    for marker in markers:
        if text.count(marker) != 1:
            print("Could not find one matching spot in gui.py. No changes were made.")
            return

    accept_from = text.find(ACCEPT_START)
    accept_to = text.find(ACCEPT_END)
    filter_from = text.find(FILTER_START)
    filter_to = text.find(FILTER_END)
    if not (accept_from < accept_to and filter_from < filter_to):
        print("The code is in an unexpected order. No changes were made.")
        return

    new_text = text[:accept_from] + NEW_ACCEPT_METHODS + text[accept_to:]
    # Recalculate the filter position, since the text above it has changed.
    filter_from = new_text.find(FILTER_START)
    filter_to = new_text.find(FILTER_END)
    new_text = new_text[:filter_from] + NEW_FILTER + new_text[filter_to:]
    compile(new_text, GUI_PATH, "exec")  # Stops here if the new code has a typo.

    shutil.copy(GUI_PATH, os.path.join(FOLDER, "gui_before_accept_change.py"))
    with open(GUI_PATH, "w", encoding="utf-8") as gui_file:
        gui_file.write(new_text)
    print("Done. Providers now see accepted requests whose collection was deleted. "
          "A backup is saved as gui_before_accept_change.py.")


if __name__ == "__main__":
    main()